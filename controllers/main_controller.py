# main_controller.py

import logging, time
import sys
import threading

import pyautogui
from PySide6.QtWidgets import QDialog

from constants.errors import LanguageError
from services.browser_manager import BrowserManager
from services.linkedin_scraper import LinkedInScraper
from services.data_manager import DataManager
from ui.message_preview_dialog import MessagePreviewDialog
from utils.utils import extract_keywords_from_search_link, get_next_message


class MainController:
    def __init__(
        self, username, password, search_link, messages_per_day,
        message_a=None, message_b=None, chatgpt_manager=None, message_type='normal', analyze_profiles=False,
        auto_reply_enabled=False, auto_reply_assistant_id=None, prospecting_assistant_id=None,
        test_mode_enabled=False,  use_ab_testing=False, account_email=None
    ):
        logging.info("Initializing MainController")
        self.browser_manager = None
        self.username = username
        self.password = password
        self.search_link = search_link
        self.messages_per_day = messages_per_day
        self.message_a = message_a
        self.message_b = message_b
        self.use_ab_testing = use_ab_testing
        self.chatgpt_manager = chatgpt_manager
        self.message_type = message_type
        self.analyze_profiles = analyze_profiles
        self.auto_reply_enabled = auto_reply_enabled
        self.auto_reply_assistant_id = auto_reply_assistant_id
        self.scraper = None
        self.data_manager = DataManager(db_path='linkedin_contacts.db')
        self.message_toggle = False  # Pour alterner entre les messages
        self.prospecting_assistant_id = prospecting_assistant_id
        self.test_mode_enabled = test_mode_enabled
        self.account_email = account_email

    def prevent_sleep(self):
        """Fonction qui permet au programme de ne pas se met en veille pendant l'execution"""
        def keep_awake():
            while True:
                pyautogui.press('shift')
                time.sleep(60)  # Répéter toutes les 60 secondes

        threading.Thread(target=keep_awake, daemon=True).start()

    def run(self):
        try:
            logging.info("Prévention de la mise en veille activée")
            self.prevent_sleep()  # Ajout pour prévenir la mise en veille

            logging.info("Starting the browser manager and LinkedIn scraper")
            self.browser_manager = BrowserManager(headless=False, block_images=False)
            self.scraper = LinkedInScraper(self.browser_manager.new_page())

            logging.info("Logging in to LinkedIn")
            self.scraper.login(self.username, self.password)
            self.scraper.ensure_authenticated()
            self.scraper.init_labels_from_language()


            # Continuer avec la prospection
            self.run_prospecting()

            # Après la prospection, si les réponses automatiques sont activées, continuer à les gérer
            if self.auto_reply_enabled:
                logging.info("Commencer à gérer les réponses automatiques en continu")
                while True:
                    try:
                        self.handle_auto_replies_sequential()
                    except Exception as e:
                        logging.error(f"Erreur lors de la gestion des réponses automatiques : {e}")
                    # Attendre avant de vérifier à nouveau
                    time.sleep(600)  # Vérifier toutes les 10 minutes
            else:
                # Si les réponses automatiques ne sont pas activées, le bot termine son exécution
                logging.info("Prospection terminée, le bot va se fermer.")
        except LanguageError as e:
            raise LanguageError(e)
        except Exception as e:
            logging.error(f"Erreur lors de l'exécution du bot : {e}")
        finally:
            # Fermer le navigateur dans tous les cas sauf si les réponses automatiques sont activées
            if not self.auto_reply_enabled:
                if self.browser_manager:
                    self.browser_manager.close()
                    logging.info("Browser manager closed")

    def run_prospecting(self):
        keywords = extract_keywords_from_search_link(self.search_link)
        self.data_manager.add_search_link(self.search_link, keywords)

        last_page_visited = self.data_manager.get_last_page_visited(self.search_link)
        logging.info(f"Last page visited: {last_page_visited}")
        self.scraper.page.goto(f"{self.search_link}&page={last_page_visited}")
        profiles = self.scraper.get_all_profiles_on_page()
        logging.info(f"Profiles found: {len(profiles)}")

        messages_sent = self.data_manager.count_messages_sent_today(self.account_email)
        logging.info(f"Messages sent today: {messages_sent}/{self.messages_per_day}")

        while messages_sent < self.messages_per_day:
            if not profiles:
                logging.info("No profiles found on this page, moving to the next page")
                if self.scraper.is_next_button_disabled():
                    logging.info("Last page reached, stopping the bot")
                    break
                else:
                    last_page_visited += 1
                    self.data_manager.update_last_page_visited(self.search_link, last_page_visited)
                    self.scraper.page.goto(f"{self.search_link}&page={last_page_visited}")
                    profiles = self.scraper.get_all_profiles_on_page()
                    logging.info(f"Profiles found: {len(profiles)} on page {last_page_visited}")
                    continue

            for profile in profiles:
                if profile is None:
                    continue

                if messages_sent >= self.messages_per_day:
                    logging.info(f"{self.account_email} a déjà atteint la limite de {self.messages_per_day} messages.")
                    return

                linkedin_profile_link = profile.get('linkedin_profile_link')
                logging.info(f"Visiting profile: {linkedin_profile_link}")

                contact_id = self.data_manager.get_contact_id(linkedin_profile_link)
                if contact_id:  # si le contact_id n'est pas None, contact déjà enregistré
                    logging.info(f"Contact {linkedin_profile_link} déjà dans la base, on passe au suivant.")
                    continue

                self.scraper.page.goto(linkedin_profile_link)
                profile_details = self.scraper.scrape_profile_details()
                if not profile_details:
                    logging.info(f"No profile details found for {linkedin_profile_link}")
                    continue

                # Mettre à jour le profil avec les détails
                profile.update(profile_details)

                # Préparer les données du profil pour le remplacement des placeholders
                profile_data = {
                    'first_name': profile.get('first_name', ''),
                    'last_name': profile.get('last_name', ''),
                    # 'full_name': profile.get('full_name', ''),
                    'title': profile.get('title', ''),
                    # 'company': profile.get('company', ''),
                    'info': profile.get('info', ''),
                    # 'experience': profile.get('experience', ''),
                    # 'position': profile.get('position', '')
                }

                # Analyser le profil si l'option est activée
                if self.analyze_profiles:
                    if not self.chatgpt_manager:
                        logging.error("ChatGPTManager n'est pas initialisé.")
                        continue
                    try:
                        # Appeler la méthode pour évaluer la pertinence du profil
                        decision = self.chatgpt_manager.evaluate_profile_relevance(profile_data)
                        if decision is None:
                            logging.error("Impossible d'évaluer le profil, passage au suivant.")
                            continue
                        elif "oui" in decision.lower():
                            logging.info("Profil pertinent, envoi du message.")
                        else:
                            logging.info("Profil non pertinent, passage au suivant.")
                            continue  # Passer au profil suivant
                    except Exception as e:
                        logging.error(f"Erreur lors de l'évaluation du profil pour {linkedin_profile_link}: {e}")
                        continue

                # **Initialiser le message généré à None**
                generated_message = None

                # **Commencer la boucle pour le mode test**
                while True:
                    # Générer le message en fonction du type de message
                    try:
                        if self.message_type == 'normal':
                            if self.use_ab_testing:
                                next_message, self.message_toggle = get_next_message(
                                    self.message_a, self.message_b, self.message_toggle
                                )
                            else:
                                # Pas d'A/B testing, on utilise toujours le message A
                                next_message = self.message_a
                            generated_message = next_message.format(**profile_data)
                        elif self.message_type == 'chatgpt':
                            if not self.chatgpt_manager or not self.prospecting_assistant_id:
                                logging.error(
                                    "ChatGPTManager ou l'Assistant ID pour la prospection n'est pas initialisé.")
                                break  # Sortir de la boucle while True
                            # Générer le message avec l'assistant via assistant ID
                            generated_message = self.chatgpt_manager.generate_response_with_assistant(
                                self.prospecting_assistant_id, profile_data
                            )
                        else:
                            logging.error(f"Type de message invalide: {self.message_type}")
                            break  # Sortir de la boucle while True
                    except Exception as e:
                        logging.error(
                            f"Erreur lors de la génération du message pour {linkedin_profile_link}: {e}")
                        break  # Sortir de la boucle while True

                    if not generated_message:
                        logging.info(f"No message generated for {linkedin_profile_link}, skipping.")
                        break  # Sortir de la boucle while True

                    # **Ajout pour le mode "test"**
                    if self.test_mode_enabled:
                        # Afficher la fenêtre de prévisualisation
                        preview_dialog = MessagePreviewDialog(generated_message)
                        result = preview_dialog.exec()

                        if result == QDialog.Accepted:
                            # L'utilisateur a accepté le message, sortir de la boucle pour envoyer le message
                            break  # Sortir de la boucle while True
                        elif result == 2:
                            # L'utilisateur a choisi "Ressayer", la boucle continue et le message sera regénéré
                            continue  # Recommencer la boucle pour regénérer le message
                        else:
                            # L'utilisateur a annulé, fermer proprement le contrôleur et l'application
                            self.close()
                            sys.exit()
                    else:
                        # Le mode test n'est pas activé, continuer normalement
                        break  # Sortir de la boucle while True

                # **Vérifier si un message a été généré et accepté**
                if generated_message:
                    # Envoyer le message
                    self.scraper.click_connect_or_more_button()
                    self.scraper.enter_custom_message(generated_message)

                    # Enregistrer l'envoi du message dans la base de données
                    self.data_manager.add_contact(
                        profile.get('full_name'),
                        profile.get('first_name'),
                        profile.get('last_name'),
                        linkedin_profile_link
                    )
                    contact_id = self.data_manager.get_contact_id(linkedin_profile_link)
                    search_id = self.data_manager.get_search_id(self.search_link)
                    self.data_manager.add_message(
                        generated_message,
                        contact_id,
                        search_id,
                        response_received=False,
                        account_email=self.account_email
                    )

                    messages_sent += 1
                    logging.info(f"{messages_sent}/{self.messages_per_day} messages sent")
                else:
                    # Si aucun message n'a été généré ou que l'utilisateur a annulé, passer au profil suivant
                    logging.info(f"Message non envoyé à {linkedin_profile_link}")
                    continue

            if messages_sent >= self.messages_per_day:
                logging.info(f"Daily message limit reached: {messages_sent}/{self.messages_per_day}")
                break

        # TODO: Des bugs sont venu a cause de cette partie, car ça vérifie le bouton next depuis une page de profil
            # if self.scraper.is_next_button_disabled():
            #     logging.info("Last page reached, stopping the bot")
            #     break

            last_page_visited += 1
            self.data_manager.update_last_page_visited(self.search_link, last_page_visited)
            self.scraper.page.goto(f"{self.search_link}&page={last_page_visited}")
            profiles = self.scraper.get_all_profiles_on_page()
            logging.info(f"Profiles found: {len(profiles)} on page {last_page_visited}")

    def handle_auto_replies_sequential(self):
        """Gère les réponses automatiques aux messages non lus, avec vérification de la cohérence de la conversation."""
        logging.info("Starting sequential handling of automatic replies")
        if not self.chatgpt_manager or not self.auto_reply_assistant_id:
            logging.error("ChatGPTManager or auto_reply_assistant_id is not initialized.")
            return

        no_new_message_count = 0
        check_interval = 20  # Commence par vérifier toutes les 2 minutes

        while True:
            self.scraper.navigate_to_unread_messages()
            unread_conversations = self.scraper.get_unread_conversations()

            if not unread_conversations:
                logging.info(f"No new unread messages. Checking again after the interval. ({check_interval} secondes)")
                no_new_message_count += 1
                # Augmenter l'intervalle après trois itérations sans nouveau message
                if no_new_message_count >= 3:
                    check_interval = 3600  # Vérifier toutes les heures après 3 fois sans nouveau message
                time.sleep(check_interval)
                continue

            no_new_message_count = 0  # Réinitialiser si un message est trouvé
            check_interval = 120  # Revenir à 2 minutes

            # Traiter la première conversation seulement
            conversation = unread_conversations[0]
            participant_name = conversation['participant_name']
            conversation_history = conversation['conversation_history']

            # Étape de vérification de la pertinence
            try:
                relevance = self.chatgpt_manager.check_message_relevance(conversation_history)
                if "non" in relevance :
                    logging.info(
                        f"Message de {participant_name} jugé hors sujet par l'assistant, aucune réponse automatique envoyée.")
                    continue  # Ne pas répondre si le message est jugé hors sujet
            except Exception as e:
                logging.error(f"Erreur lors de la vérification de la pertinence pour {participant_name}: {e}")
                continue

            # Générer la réponse automatique uniquement si la pertinence est confirmée
            try:
                thread_id = self.chatgpt_manager.create_thread()
                if not thread_id:
                    logging.error("Échec de la création du thread.")
                    continue

                # Ajouter l'historique de la conversation au thread
                for message in conversation_history:
                    self.chatgpt_manager.add_message_to_thread(thread_id, message['message'])

                # Exécuter l'assistant sur le thread
                run_id = self.chatgpt_manager.run_assistant(thread_id, self.auto_reply_assistant_id)
                if not run_id:
                    logging.error("Échec de l'exécution de l'assistant.")
                    continue

                # Attendre que l'assistant ait terminé de générer la réponse
                time.sleep(5)

                # Récupérer la réponse de l'assistant
                assistant_response = self.chatgpt_manager.get_assistant_response(thread_id)
                if assistant_response:
                    # Envoyer la réponse sur LinkedIn
                    self.scraper.send_reply(assistant_response)
                    logging.info(f"Réponse automatique envoyée à {participant_name}")
                else:
                    logging.error(f"Aucune réponse de l'assistant pour {participant_name}")
            except Exception as e:
                logging.error(f"Erreur lors de la génération de la réponse pour {participant_name}: {e}")

            # Pause avant de vérifier les nouveaux messages
            time.sleep(check_interval)


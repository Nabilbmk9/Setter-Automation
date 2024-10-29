# main_controller.py

import logging

from constants.errors import LanguageError
from services.browser_manager import BrowserManager
from services.linkedin_scraper import LinkedInScraper
from services.data_manager import DataManager
from utils.utils import extract_keywords_from_search_link, get_next_message


class MainController:
    def __init__(
        self, username, password, search_link, messages_per_day,
        message_a=None, message_b=None, chatgpt_manager=None, message_type='normal'
    ):
        logging.info("Initializing MainController")
        self.browser_manager = None
        self.username = username
        self.password = password
        self.search_link = search_link
        self.messages_per_day = messages_per_day
        self.message_a = message_a
        self.message_b = message_b
        self.chatgpt_manager = chatgpt_manager
        self.message_type = message_type
        self.scraper = None
        self.data_manager = DataManager(db_path='linkedin_contacts.db')
        self.message_toggle = False  # Pour alterner entre les messages

    def run(self):
        try:
            logging.info("Starting the browser manager and LinkedIn scraper")
            self.browser_manager = BrowserManager(headless=False, block_images=False)
            self.scraper = LinkedInScraper(self.browser_manager.new_page())

            logging.info("Logging in to LinkedIn")
            self.scraper.login(self.username, self.password)
            self.scraper.ensure_authenticated()
            self.scraper.init_labels_from_language()

            keywords = extract_keywords_from_search_link(self.search_link)
            self.data_manager.add_search_link(self.search_link, keywords)

            last_page_visited = self.data_manager.get_last_page_visited(self.search_link)
            logging.info(f"Last page visited: {last_page_visited}")
            self.scraper.page.goto(f"{self.search_link}&page={last_page_visited}")
            profiles = self.scraper.get_all_profiles_on_page()
            logging.info(f"Profiles found: {len(profiles)}")

            messages_sent = self.data_manager.count_messages_sent_today()
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
                        logging.info(f"Daily message limit reached: {messages_sent}/{self.messages_per_day}")
                        return

                    linkedin_profile_link = profile.get('linkedin_profile_link')
                    logging.info(f"Visiting profile: {linkedin_profile_link}")
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
                        'full_name': profile.get('full_name', ''),
                        'title': profile.get('title', ''),
                        'company': profile.get('company', ''),
                        'info': profile.get('info', ''),
                        'experience': profile.get('experience', ''),
                        'position': profile.get('position', '')
                    }

                    # Générer le message en fonction du type de message
                    try:
                        if self.message_type == 'normal':
                            next_message, self.message_toggle = get_next_message(
                                self.message_a, self.message_b, self.message_toggle
                            )
                            # Remplacer les variables dans le message
                            next_message = next_message.format(**profile_data)
                            generated_message = next_message
                        elif self.message_type == 'chatgpt':
                            if not self.chatgpt_manager:
                                logging.error("ChatGPTManager n'est pas initialisé.")
                                continue
                            # Remplacer les placeholders dans le prompt
                            prompt_template = self.chatgpt_manager.prompt_template
                            formatted_prompt = prompt_template.format(**profile_data)
                            # Générer le message avec ChatGPT
                            generated_message = self.chatgpt_manager.generate_response(formatted_prompt)
                        else:
                            logging.error(f"Type de message invalide: {self.message_type}")
                            continue
                    except Exception as e:
                        logging.error(
                            f"Erreur lors de la génération du message pour {linkedin_profile_link}: {e}")
                        continue

                    if not generated_message:
                        logging.info(f"No message generated for {linkedin_profile_link}, skipping.")
                        continue

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
                    self.data_manager.add_message(generated_message, contact_id, search_id)

                    messages_sent += 1
                    logging.info(f"{messages_sent}/{self.messages_per_day} messages sent")

                    if messages_sent >= self.messages_per_day:
                        logging.info(f"Daily message limit reached: {messages_sent}/{self.messages_per_day}")
                        break

                if self.scraper.is_next_button_disabled():
                    logging.info("Last page reached, stopping the bot")
                    break

                last_page_visited += 1
                self.data_manager.update_last_page_visited(self.search_link, last_page_visited)
                self.scraper.page.goto(f"{self.search_link}&page={last_page_visited}")
                profiles = self.scraper.get_all_profiles_on_page()
                logging.info(f"Profiles found: {len(profiles)} on page {last_page_visited}")

        except LanguageError as e:
            raise LanguageError(e)
        except Exception as e:
            logging.error(f"Error running the bot: {e}")
        finally:
            if self.browser_manager:
                self.browser_manager.close()
                logging.info("Browser manager closed")

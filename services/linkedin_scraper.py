import random
import time

from constants.errors import LanguageError
from constants.labels import LABELS
from utils.utils import remove_emojis
from config.logging_config import setup_logging

logger = setup_logging()


class LinkedInScraper:
    def __init__(self, page):
        self.page = page
        self.page.goto("https://www.linkedin.com/login")

        self.labels = None
        self.init_labels_from_language()

        logger.info("LinkedInScraper initialized")

    def login(self, username, password):
        self.page.get_by_label(self.labels["email_or_phone"]).fill(username)
        self.page.get_by_label(self.labels["password"]).fill(password)
        self.page.get_by_label(self.labels["login"], exact=True).click()
        logger.info("Login effectué")

    def ensure_authenticated(self):
        # Boucle pour vérifier les différents types de vérification
        while self._check_for_email_verification_pin() or self._check_for_verification_page() or self._check_for_captcha_challenge():
            logger.info("En attente que l'utilisateur résolve la vérification manuelle ou entre un code PIN...")
            # Mettre en pause pour permettre à l'utilisateur de résoudre la vérification manuellement
            self.page.wait_for_timeout(10000)  # Pause de 10 secondes entre chaque vérification
        logger.info("Authentification vérifiée")

    def get_all_profiles_on_page(self):
        self.page.wait_for_selector('div[data-view-name="search-entity-result-universal-template"]')
        all_profiles_list = self._fetch_profiles_list()
        all_profiles_info = [
            self._extract_profile_info(profile_content)
            for profile_content in all_profiles_list
        ]
        # Filtrer les profils non valides
        all_profiles_info = [info for info in all_profiles_info if info is not None]
        logger.info(f"{len(all_profiles_info)} profils trouvés sur la page")
        return all_profiles_info

    def click_connect_or_more_button(self):
        """Gère le clic sur 'Se connecter' ou 'Plus' pour accéder à 'Se connecter'."""
        action_buttons, button_texts = self._get_profile_action_buttons()

        # Essayer de cliquer sur "Se connecter"
        if self._click_button_by_text(action_buttons, self.labels["connect"]):
            logger.info("Bouton 'Se connecter' cliqué")
            self._click_add_note_button()
            return

        # Sinon, cliquer sur "Plus" puis "Se connecter" dans le menu déroulant
        if self._click_button_by_text(action_buttons, self.labels["plus"]):
            logger.info("Bouton 'Plus' cliqué")
            if self._click_connect_button_from_dropdown():
                logger.info("Bouton 'Se connecter' cliqué dans le menu déroulant")
                self._click_add_note_button()

    def enter_custom_message(self, message):
        """Écrit le message généré dans le champ de texte."""
        try:
            self.page.wait_for_selector('textarea[name="message"]', timeout=5000)
            message_textarea = self.page.query_selector('textarea[name="message"]')
            if message_textarea:
                message_textarea.fill(message)
                logger.info("Message personnalisé écrit")
                self._click_send_invitation_button()
            else:
                logger.error("Textarea non trouvé")
        except Exception as e:
            logger.error(f"Erreur lors de la sélection du textarea : {e}")

    def is_next_button_disabled(self):
        try:
            next_button = self.page.query_selector('button.artdeco-pagination__button--next')
            return next_button and 'artdeco-button--disabled' in next_button.get_attribute('class')
        except Exception as e:
            logger.error(f"Erreur lors de la vérification du bouton suivant : {e}")
            return False

    def scrape_profile_details(self):
        """Scrape the profile details for additional information."""
        try:
            # Attendre que la page soit complètement chargée
            self.page.wait_for_load_state('load')

            profile_details = {
                "title": self._scrape_title(),
                "info": self._scrape_info(),
                "experience": self._scrape_experience()
            }
            return profile_details

        except Exception as e:
            logger.error(f"Erreur lors de l'extraction des détails du profil : {e}")
            return {}

    # Méthodes privées

    def _scrape_title(self):
        """Scrape the title from the profile page."""
        try:
            title_element = self.page.query_selector('.text-body-medium')
            return title_element.inner_text().strip() if title_element else "Non spécifié"
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du titre : {e}")
            return "Non spécifié"

    def _scrape_info(self):
        """Scrape the information section from the profile page."""
        try:
            # Cibler le conteneur principal de la section "Infos"
            info_container = self.page.query_selector(
                '.pv-profile-card.break-words .display-flex.ph5.pv3 .inline-show-more-text--is-collapsed')

            # Extraire le texte de la section "Infos"
            if info_container:
                info_text = info_container.query_selector('span[aria-hidden="true"]').inner_text().strip()
                return info_text
            else:
                logger.info("Aucune section 'Infos' trouvée")
                return "Non spécifié"
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la partie information : {e}")
            return "Non spécifié"

    # TODO revoir toute la fonction
    def _scrape_experience(self):
        try:
            # Sélectionner les sections d'expérience
            experience_sections = self.page.query_selector_all('section:has(div#experience) ul li')
            experiences = []

            for item in experience_sections:
                # Extraire les informations de base pour l'expérience principale
                experience = {
                    'title': self._extract_experience_title(item),
                    'company': self._extract_experience_company(item),
                    'period': self._extract_experience_period(item),
                    'location': self._extract_experience_location(item),
                    'description': self._extract_experience_description(item)
                }
                # Vérifier les sous-expériences
                sub_experiences = self._extract_sub_experiences(item)
                if sub_experiences:
                    experience['sub_experiences'] = sub_experiences

                # Ajouter à la liste des expériences
                experiences.append(experience)

            return experiences if experiences else "Non spécifié"
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des expériences : {e}")
            return "Non spécifié"

    def _extract_experience_title(self, item):
        try:
            # Rechercher le titre du poste
            title_element = item.query_selector('.t-bold') or item.query_selector('.hoverable-link-text')
            return title_element.inner_text().strip() if title_element else "Non spécifié"
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du titre : {e}")
            return "Non spécifié"

    def _extract_experience_company(self, item):
        try:
            # Rechercher le nom de l'entreprise
            company_element = item.query_selector('.t-14.t-normal') or item.query_selector('.hoverable-link-text')
            return company_element.inner_text().strip() if company_element else "Non spécifié"
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'entreprise : {e}")
            return "Non spécifié"

    def _extract_experience_period(self, item):
        try:
            # Rechercher la période de travail
            period_element = item.query_selector('.t-14.t-normal.t-black--light') or item.query_selector(
                '.pvs-entity__caption-wrapper')
            return period_element.inner_text().strip() if period_element else "Non spécifié"
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la période : {e}")
            return "Non spécifié"

    def _extract_experience_location(self, item):
        try:
            # Rechercher le lieu de l'expérience
            location_element = item.query_selector('.t-14.t-normal.t-black--light')
            return location_element.inner_text().strip() if location_element else "Non spécifié"
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du lieu : {e}")
            return "Non spécifié"

    def _extract_experience_description(self, item):
        try:
            # Rechercher la description de l'expérience
            description_element = item.query_selector('.t-14.t-normal.t-black') or item.query_selector(
                '.display-flex.t-14')
            return description_element.inner_text().strip() if description_element else "Non spécifié"
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la description : {e}")
            return "Non spécifié"

    def _extract_sub_experiences(self, item):
        try:
            # Rechercher les sous-expériences
            sub_experience_elements = item.query_selector_all('.pvs-entity__sub-components li')
            sub_experiences = []

            for sub_item in sub_experience_elements:
                sub_experience = {
                    'title': self._extract_experience_title(sub_item),
                    'company': self._extract_experience_company(sub_item),
                    'period': self._extract_experience_period(sub_item),
                    'location': self._extract_experience_location(sub_item),
                    'description': self._extract_experience_description(sub_item)
                }
                sub_experiences.append(sub_experience)

            return sub_experiences if sub_experiences else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des sous-expériences : {e}")
            return None

    def _check_for_email_verification_pin(self):
        try:
            self.page.wait_for_selector('#input__email_verification_pin', timeout=5000)
            logger.info("Page d'authentification détectée avec ID. En attente du code de vérification.")
            return True
        except:
            return False

    def _check_for_verification_page(self):
        """Vérifie si la page de demande de vérification est présente et clique sur 'Vérifier'."""
        try:
            # Vérifier si le texte "Vérification" est présent sur la page
            verification_element = self.page.query_selector('h2#home_children_heading')
            if verification_element and verification_element.inner_text() == "Vérification":
                logger.info("Page de vérification détectée. Tentative de clic sur 'Vérifier'.")
                # Cliquer sur le bouton "Vérifier"
                verify_button = self.page.query_selector('#home_children_button')
                if verify_button:
                    verify_button.click()
                    logger.info("Bouton 'Vérifier' cliqué.")
                    return True
            return False
        except Exception as e:
            logger.error(f"Erreur lors de la vérification de la page 'Vérifier' : {e}")
            return False

    def _check_for_captcha_challenge(self):
        """Vérifie si le captcha ou l'énigme est présent dans un iframe."""
        try:
            # Vérifier si l'iframe du captcha est présente
            captcha_iframe = self.page.query_selector('#captcha-internal')
            if captcha_iframe:
                logger.info("Iframe captcha détectée. En attente de la résolution du captcha.")
                return True
            return False
        except Exception as e:
            logger.error(f"Erreur lors de la vérification du captcha : {e}")
            return False

    def _fetch_profiles_list(self):
        return self.page.query_selector_all('div[data-view-name="search-entity-result-universal-template"]')

    def _extract_profile_info(self, profile_content):
        # Étape 1: Trouver le bouton 'Connect' ou 'Pending'
        action_button = profile_content.query_selector('button.artdeco-button')
        if not action_button:
            return None
        connect_or_follow = action_button.inner_text().strip()
        if connect_or_follow not in self.labels["connect_or_follow"]:
            return None

        # Étape 2: Obtenir le lien du profil
        linkedin_profile_link_element = profile_content.query_selector('a[href*="/in/"]')
        if not linkedin_profile_link_element:
            return None
        linkedin_profile_link = linkedin_profile_link_element.get_attribute('href')

        # Étape 3: Obtenir le nom complet
        full_name_element = profile_content.query_selector('a[href*="/in/"] span[dir="ltr"] span[aria-hidden="true"]')
        if not full_name_element:
            return None
        full_name = full_name_element.inner_text().strip()
        full_name = remove_emojis(full_name)

        # Extraction du prénom et du nom
        name_parts = full_name.split()
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ""

        return {
            "full_name": full_name,
            "first_name": first_name,
            "last_name": last_name,
            "linkedin_profile_link": linkedin_profile_link,
            "connect_or_follow": connect_or_follow
        }

    def _get_profile_action_buttons(self):
        """Récupère les boutons d'action de profil et leurs textes."""
        action_buttons = self.page.query_selector_all('.pvs-profile-actions__action')

        button_texts = [button.inner_text().strip() for button in action_buttons]

        return action_buttons, button_texts

    def _click_button_by_text(self, action_buttons, button_text):
        """Clique sur le bouton avec le texte spécifié."""
        for button in action_buttons:
            text = button.inner_text().strip()
            if text == button_text:
                button.click()
                return True
        return False

    def _click_connect_button_from_dropdown(self):
        """Clique sur le bouton 'Se connecter' dans le menu déroulant."""
        self.page.wait_for_timeout(1000)  # Attendre que le menu déroulant apparaisse
        dropdown_buttons = self.page.query_selector_all('.artdeco-dropdown__item--is-dropdown')
        for dropdown_button in dropdown_buttons:
            dropdown_text = dropdown_button.inner_text().strip()
            if dropdown_text == self.labels['connect']:
                dropdown_button.click()
                return True
        return False

    def _click_add_note_button(self):
        """Clique sur le bouton 'Ajouter une note' après avoir cliqué sur 'Se connecter'."""
        self.page.wait_for_timeout(1000)  # Attendre que le bouton apparaisse
        add_note_button = self.page.query_selector(f'button[aria-label="{self.labels["add_a_note"]}"]')
        if add_note_button:
            add_note_button.click()

    def _click_send_invitation_button(self):
        """Clique sur le bouton 'Envoyer' après avoir écrit le message."""
        self.page.wait_for_timeout(1000)  # Attendre que le bouton apparaisse
        send_button = self.page.query_selector(f'button[aria-label="{self.labels["send_invitation"]}"]')
        if send_button:
            send_button.click()
            logger.info("Invitation envoyée")
            # Ajouter un délai aléatoire entre 1 et 3 secondes après avoir envoyé un message
            delay = random.randint(7, 15)
            time.sleep(delay)
        else:
            logger.error("Bouton 'Envoyer une invitation' non trouvé")

    def navigate_to_unread_messages(self):
        """Navigue vers la page des messages non lus et recharge si nécessaire."""
        self.page.goto("https://www.linkedin.com/messaging/?filter=unread")
        self.page.wait_for_selector('.msg-conversations-container__conversations-list')
        logger.info("Navigué vers la page des messages non lus")

    def get_unread_conversations(self):
        """Récupère la première conversation non lue seulement."""
        unread_conversations = []
        conversation_items = self.page.query_selector_all(
            '.msg-conversations-container__convo-item .msg-conversation-card__convo-item-container--unread'
        )

        if conversation_items:
            conversation = conversation_items[0]  # Ne traiter que la première conversation non lue
            try:
                # Extraire le nom et le lien de la conversation
                participant_name = conversation.query_selector(
                    '.msg-conversation-listitem__participant-names span.truncate'
                ).inner_text().strip()

                # Cliquez sur la conversation pour l'ouvrir
                conversation.click()
                self.page.wait_for_selector('.msg-s-message-list__event')

                # Extraire l'historique complet de la conversation en scrollant
                conversation_history = self.get_conversation_history()

                # Ajouter les informations de la conversation non lue
                unread_conversations.append({
                    'participant_name': participant_name,
                    'conversation_history': conversation_history
                })

                logger.info(f"Première conversation non lue récupérée pour : {participant_name}")
            except Exception as e:
                logger.error(f"Erreur lors de la récupération de la conversation : {e}")

        return unread_conversations

    def get_conversation_history(self):
        """Récupère l'historique complet des messages dans une conversation ouverte."""
        messages = []
        last_height = 0

        while True:
            # Scroller vers le haut pour charger les messages précédents
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Pause pour permettre le chargement des messages

            # Vérifier la hauteur de défilement pour voir si on a atteint le haut
            current_height = self.page.evaluate("document.body.scrollHeight")
            if current_height == last_height:
                break  # Sortir de la boucle si plus de messages ne se chargent
            last_height = current_height

        # Sélection de tous les éléments de messages dans la conversation
        message_elements = self.page.query_selector_all('.msg-s-message-list__event')

        for message_element in message_elements:
            try:
                # Extraire l'auteur du message
                author_element = message_element.query_selector('.msg-s-message-group__name')
                author = author_element.inner_text().strip() if author_element else "Inconnu"

                # Extraire le texte du message
                text_element = message_element.query_selector('.msg-s-event-listitem__body')
                text = text_element.inner_text().strip() if text_element else ""

                # Ajouter chaque message avec son auteur dans la liste
                if text:  # Ignorer les messages vides
                    messages.append({"author": author, "message": text})

            except Exception as e:
                logger.error(f"Erreur lors de l'extraction du message : {e}")

        return messages

    def send_reply(self, reply_message):
        """Envoie un message de réponse dans la conversation ouverte."""
        try:
            # Sélectionner le champ de texte pour écrire le message
            message_box = self.page.query_selector('.msg-form__contenteditable')
            if message_box:
                message_box.fill(reply_message)
                logger.info("Message de réponse rempli")

                # Cliquer sur le bouton d'envoi
                send_button = self.page.query_selector('button.msg-form__send-button')
                if send_button:
                    send_button.click()
                    logger.info("Message de réponse envoyé")
            else:
                logger.error("Impossible de trouver le champ de message")
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de la réponse : {e}")

    """
    Cette fonction doit être appelée avant le login et apres la connexion car la langue peut etre différente entre 
    l'ouverture initiale de LinkedIn et après la connection de l'utilisateur car la langue de la page devient celle du 
    profil de l'utilisateur. 
    """
    def init_labels_from_language(self):
        language = self.page.evaluate("document.documentElement.lang")
        normalized_language = language.split('-')[0]

        if normalized_language in LABELS:
            self.labels = LABELS[normalized_language]
        else:
            logger.error(f"Langue du profil LinkedIn non supportée : {language}")
            raise LanguageError(f"Langue du profil LinkedIn non supportée : {language}")

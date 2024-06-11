import logging
from src.utils import remove_emojis

# Configurer le logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LinkedInScraper:
    def __init__(self, page):
        self.page = page

    # Méthodes publiques
    def login(self, username, password):
        self.page.goto("https://www.linkedin.com/login")
        self.page.get_by_label("E-mail ou téléphone").fill(username)
        self.page.get_by_label("Mot de passe").fill(password)
        self.page.get_by_label("S’identifier", exact=True).click()
        logger.info("Login effectué")

    def ensure_authenticated(self):
        while self._check_for_email_verification_pin():
            self.page.wait_for_timeout(10000)
        logger.info("Authentification vérifiée")

    def get_all_profiles_on_page(self):
        self.page.wait_for_selector('li.reusable-search__result-container')
        all_profiles_list = self._fetch_profiles_list()
        all_profiles_info = [self._extract_profile_info(profile_content) for profile_content in all_profiles_list]
        logger.info(f"{len(all_profiles_info)} profils trouvés sur la page")
        return all_profiles_info

    def click_connect_or_more_button(self):
        """Gère le clic sur 'Se connecter' ou 'Plus' pour accéder à 'Se connecter'."""
        action_buttons, button_texts = self._get_profile_action_buttons()

        # Essayer de cliquer sur "Se connecter"
        if self._click_button_by_text(action_buttons, "Se connecter"):
            logger.info("Bouton 'Se connecter' cliqué")
            self._click_add_note_button()
            return

        # Sinon, cliquer sur "Plus" puis "Se connecter" dans le menu déroulant
        if self._click_button_by_text(action_buttons, "Plus"):
            logger.info("Bouton 'Plus' cliqué")
            if self._click_connect_button_from_dropdown():
                logger.info("Bouton 'Se connecter' cliqué dans le menu déroulant")
                self._click_add_note_button()

    def enter_custom_message(self, first_name, message_template):
        """Remplace {first_name} dans le message et l'écrit dans le textarea."""
        custom_message = message_template.replace("{first_name}", first_name)
        try:
            self.page.wait_for_selector('textarea[name="message"]', timeout=5000)  # Attendre que le textarea soit visible
            message_textarea = self.page.query_selector('textarea[name="message"]')
            if message_textarea:
                message_textarea.fill(custom_message)
                logger.info(f"Message personnalisé écrit pour {first_name}")
                self._click_send_invitation_button()
            else:
                logger.error("Textarea non trouvé")
        except Exception as e:
            logger.error(f"Erreur lors de la sélection du textarea : {e}")

    # Méthodes privées
    def _check_for_email_verification_pin(self):
        try:
            self.page.wait_for_selector('#input__email_verification_pin', timeout=5000)
            logger.info("Page d'authentification détectée avec ID. En attente du code de vérification.")
            return True
        except:
            return False

    def _fetch_profiles_list(self):
        return self.page.query_selector_all('li.reusable-search__result-container')

    def _extract_profile_info(self, profile_content):
        connect_or_follow = profile_content.query_selector('div.entity-result__actions.entity-result__divider').inner_text()
        if connect_or_follow not in ["Se connecter", "Suivre"]:
            return None
        linkedin_profile_link = profile_content.query_selector('a').get_attribute('href')

        # Modification ici pour le nom complet
        full_name_element = profile_content.query_selector('span.entity-result__title-text a span[dir="ltr"]')
        full_name = full_name_element.inner_text().strip()  # Retire les espaces superflus
        full_name = remove_emojis(full_name)  # Enlève les emojis si nécessaire

        # Extraction du prénom et du nom si possible
        name_parts = full_name.split()
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        return {
            "full_name": f"{first_name} {last_name}",
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
            if dropdown_text == "Se connecter":
                dropdown_button.click()
                return True
        return False

    def _click_add_note_button(self):
        """Clique sur le bouton 'Ajouter une note' après avoir cliqué sur 'Se connecter'."""
        self.page.wait_for_timeout(1000)  # Attendre que le bouton apparaisse
        add_note_button = self.page.query_selector('button[aria-label="Ajouter une note"]')
        if add_note_button:
            add_note_button.click()

    def _click_send_invitation_button(self):
        """Clique sur le bouton 'Envoyer' après avoir écrit le message."""
        self.page.wait_for_timeout(1000)  # Attendre que le bouton apparaisse
        send_button = self.page.query_selector('button[aria-label="Envoyer une invitation"]')
        if send_button:
            send_button.click()
            logger.info("Invitation envoyée")
        else:
            logger.error("Bouton 'Envoyer une invitation' non trouvé")


    def _load_all_messages(self):
        # Attente explicite pour que la page se charge initialement
        self.page.wait_for_selector('.msg-conversation-listitem', state='attached')

        # Récupération du nombre initial de conversations visibles
        initial_count = self.page.locator('.msg-conversation-listitem').count()

        while True:
            try:
                load_more_button = self.page.locator('text=Charger plus de conversations')
                if load_more_button.is_visible():
                    load_more_button.click()
                    # Attente pour que de nouveaux messages soient chargés
                    self.page.wait_for_timeout(2000)

                    # Vérifier si le nombre de messages a augmenté
                    current_count = self.page.locator('.msg-conversation-listitem').count()
                    if current_count == initial_count:
                        # Si le nombre de messages n'a pas augmenté, arrêter de charger
                        break
                    else:
                        # Mettre à jour le nombre initial pour la prochaine itération
                        initial_count = current_count
                else:
                    break
            except Exception as e:
                print(f"Exception occurred while loading messages: {e}")
                break


from src.utils import remove_emojis


class LinkedInScraper:
    def __init__(self, page):
        self.page = page

    def login(self, username, password):
        self.page.goto("https://www.linkedin.com/login")
        self.page.get_by_label("E-mail ou téléphone").fill(username)
        self.page.get_by_label("Mot de passe").fill(password)
        self.page.get_by_label("S’identifier", exact=True).click()

    def check_for_email_verification_pin(self):
        try:
            self.page.wait_for_selector('#input__email_verification_pin', timeout=5000)
            print("Page d'authentification détectée avec ID. En attente du code de vérification.")
            return True
        except:
            return False

    def ensure_authenticated(self):
        while self.check_for_email_verification_pin():
            self.page.wait_for_timeout(10000)

    def fetch_unread_messages(self):
        self.page.get_by_role("link", name="Messagerie").click()
        self.page.get_by_role("radio", name="Non lus").click()
        self._load_all_messages()

    def get_all_profiles_on_page(self):
        self.page.wait_for_selector('li.reusable-search__result-container')
        all_profiles_list = self._fetch_profiles_list()
        all_profiles_info = [self._extract_profile_info(profile_content) for profile_content in all_profiles_list]
        print(all_profiles_info)
        return all_profiles_info

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
            "full_name": full_name,
            "first_name": first_name,
            "last_name": last_name,
            "linkedin_profile_link": linkedin_profile_link,
            "connect_or_follow": connect_or_follow
        }

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


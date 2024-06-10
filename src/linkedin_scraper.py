class LinkedInScraper:
    def __init__(self, page):
        self.page = page

    def login(self, username, password):
        self.page.goto("https://www.linkedin.com/login")
        self.page.get_by_label("E-mail ou téléphone").fill(username)
        self.page.get_by_label("Mot de passe").fill(password)
        self.page.get_by_label("S’identifier", exact=True).click()

    #TODO check if there is suspect verification
    def suspect_verification(self):
        if self.page.get_by_placeholder("Saisissez le code"):
            print("hello")

    def fetch_unread_messages(self):
        self.page.get_by_role("link", name="Messagerie").click()
        self.page.get_by_role("radio", name="Non lus").click()
        self._load_all_messages()

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


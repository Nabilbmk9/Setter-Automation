import logging

from browser_manager import BrowserManager
from linkedin_scraper import LinkedInScraper
# from chatgpt_manager import ChatGPTManager
from data_manager import DataManager
from src.utils import extract_keywords_from_search_link, get_env_variable, get_next_message

import threading
from gmail_api import run_email_checker


class MainController:
    def __init__(self):
        self.browser_manager = BrowserManager(headless=False, block_images=False)
        self.username = get_env_variable('LINKEDIN_EMAIL')
        self.password = get_env_variable('LINKEDIN_PASSWORD')
        self.search_link = get_env_variable('LINKEDIN_SEARCH_LINK')
        self.message_a = get_env_variable('MESSAGE_A')
        self.message_b = get_env_variable('MESSAGE_B')
        self.api_key = get_env_variable('GPT_API_KEY')
        self.messages_per_day = int(get_env_variable('MESSAGES_PER_DAY', 10))
        self.scraper = LinkedInScraper(self.browser_manager.new_page())
        # self.chat_manager = ChatGPTManager(api_key=self.api_key)
        self.data_manager = DataManager(db_path='linkedin_contacts.db')
        self.message_toggle = False  # Pour alterner entre les messages

    def run(self):
        self.scraper.login(self.username, self.password)
        self.scraper.ensure_authenticated()

        # Extraire les mots-clés du lien de recherche
        keywords = extract_keywords_from_search_link(self.search_link)

        # Ajout de la recherche
        self.data_manager.add_search_link(self.search_link, keywords)
        last_page_visited = self.data_manager.get_last_page_visited(self.search_link)
        self.scraper.page.goto(f"{self.search_link}&page={last_page_visited}")

        profiles = self.scraper.get_all_profiles_on_page()
        messages_sent = self.data_manager.count_messages_sent_today()

        for profile in profiles:
            if profile:
                if messages_sent >= self.messages_per_day:
                    logging.info("Limite de messages par jour atteinte, arrêt du bot")
                    break

                self.scraper.page.goto(profile.get('linkedin_profile_link'))
                profile_details = self.scraper.scrape_profile_details()
                profile.update(profile_details)  # Ajouter les détails au profil
                self.scraper.click_connect_or_more_button()
                next_message, self.message_toggle = get_next_message(self.message_a, self.message_b, self.message_toggle)
                self.scraper.enter_custom_message(profile.get('first_name'), next_message)

                # Enregistrement du contact et du message
                self.data_manager.add_contact(
                    profile.get('full_name'),
                    profile.get('first_name'),
                    profile.get('last_name'),
                    profile.get('linkedin_profile_link')
                )
                contact_id = self.data_manager.get_contact_id(profile.get('linkedin_profile_link'))
                search_id = self.data_manager.get_search_id(self.search_link)
                self.data_manager.add_message(next_message, contact_id, search_id)

                messages_sent += 1
                logging.info(f"{messages_sent}/{self.messages_per_day} messages envoyés")

        self.data_manager.update_last_page_visited(self.search_link, last_page_visited + 1)
        self.browser_manager.close()


# Démarrer le vérificateur d'emails en arrière-plan
email_thread = threading.Thread(target=run_email_checker, daemon=True)
email_thread.start()

if __name__ == '__main__':
    controller = MainController()
    controller.run()

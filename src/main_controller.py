from browser_manager import BrowserManager
from linkedin_scraper import LinkedInScraper
# from chatgpt_manager import ChatGPTManager
from data_manager import DataManager
from config import get_env_variable
from src.utils import extract_keywords_from_search_link


class MainController:
    def __init__(self):
        self.browser_manager = BrowserManager(headless=False, block_images=False)
        self.username = get_env_variable('LINKEDIN_EMAIL')
        self.password = get_env_variable('LINKEDIN_PASSWORD')
        self.search_link = get_env_variable('LINKEDIN_SEARCH_LINK')
        self.message_template = get_env_variable('MESSAGE')
        self.api_key = get_env_variable('GPT_API_KEY')
        self.scraper = LinkedInScraper(self.browser_manager.new_page())
        # self.chat_manager = ChatGPTManager(api_key=self.api_key)
        self.data_manager = self.data_manager = DataManager(db_path='linkedin_contacts.db')

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
        for profile in profiles:
            if profile:
                self.scraper.page.goto(profile.get('linkedin_profile_link'))
                self.scraper.click_connect_or_more_button()
                self.scraper.enter_custom_message(profile.get('first_name'), self.message_template)

                # Enregistrement du contact et du message
                self.data_manager.add_contact(
                    profile.get('full_name'),
                    profile.get('first_name'),
                    profile.get('last_name'),
                    profile.get('linkedin_profile_link')
                )
                contact_id = self.data_manager.get_contact_id(profile.get('linkedin_profile_link'))
                search_id = self.data_manager.get_search_id(self.search_link)
                self.data_manager.add_message(self.message_template, contact_id, search_id)

        self.data_manager.update_last_page_visited(self.search_link, last_page_visited + 1)
        self.browser_manager.close()


if __name__ == '__main__':
    controller = MainController()
    controller.run()

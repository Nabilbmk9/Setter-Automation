from browser_manager import BrowserManager
from linkedin_scraper import LinkedInScraper
# from chatgpt_manager import ChatGPTManager
from data_manager import DataManager
from config import get_env_variable


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
        self.data_manager = DataManager(db_connection='your_database_connection_string')

    def run(self):
        self.scraper.login(self.username, self.password)
        self.scraper.ensure_authenticated()
        self.scraper.page.goto(self.search_link)

        profiles = self.scraper.get_all_profiles_on_page()
        for profile in profiles:
            if profile:
                self.scraper.page.goto(profile.get('linkedin_profile_link'))
                self.scraper.click_connect_or_more_button()
                self.scraper.enter_custom_message(profile.get('first_name'), self.message_template)

        # self.scraper.fetch_unread_messages()
                self.browser_manager.close()


if __name__ == '__main__':
    controller = MainController()
    controller.run()

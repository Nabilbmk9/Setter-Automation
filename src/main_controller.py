from browser_manager import BrowserManager
from linkedin_scraper import LinkedInScraper
from chatgpt_manager import ChatGPTManager
from data_manager import DataManager
from config import get_env_variable


class MainController:
    def __init__(self):
        self.browser_manager = BrowserManager(headless=False, block_images=False)
        self.scraper = LinkedInScraper(self.browser_manager.new_page())
        self.chat_manager = ChatGPTManager(api_key='your_chatgpt_api_key')
        self.data_manager = DataManager(db_connection='your_database_connection_string')
        self.username = get_env_variable('LINKEDIN_USERNAME')
        self.password = get_env_variable('LINKEDIN_PASSWORD')

    def run(self):
        self.scraper.login(self.username, self.password)
        self.scraper.fetch_unread_messages()
        self.browser_manager.close()


if __name__ == '__main__':
    controller = MainController()
    controller.run()
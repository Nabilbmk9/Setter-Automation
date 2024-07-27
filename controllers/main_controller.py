import logging

from constants.errors import LanguageError
from services.browser_manager import BrowserManager
from services.linkedin_scraper import LinkedInScraper
from services.data_manager import DataManager
from utils.utils import extract_keywords_from_search_link, get_next_message


class MainController:
    def __init__(self, state_checkbox_google, username, password, search_link, message_a, message_b, messages_per_day):
        logging.info("Initializing MainController")
        self.browser_manager = None
        self.state_checkbox_google = state_checkbox_google
        self.username = username
        self.password = password
        self.search_link = search_link
        self.message_a = message_a
        self.message_b = message_b
        self.messages_per_day = messages_per_day
        self.scraper = None
        self.data_manager = DataManager(db_path='linkedin_contacts.db')
        self.message_toggle = False  # Pour alterner entre les messages

    def run(self):
        try:
            logging.info("Starting the browser manager and LinkedIn scraper")
            self.browser_manager = BrowserManager(headless=False, block_images=False)
            self.scraper = LinkedInScraper(self.browser_manager.new_page())

            logging.info("Logging in to LinkedIn")
            self.scraper.login(self.state_checkbox_google, self.username, self.password)
            self.scraper.ensure_authenticated()
            self.scraper.init_labels_from_language()

            keywords = extract_keywords_from_search_link(self.search_link)
            self.data_manager.add_search_link(self.search_link, keywords)

            last_page_visited = self.data_manager.get_last_page_visited(self.search_link)
            logging.info(f"Last page visited: {last_page_visited}")
            self.scraper.page.goto(f"{self.search_link}&page={last_page_visited}")
            profiles = self.scraper.get_all_profiles_on_page()
            logging.info(f"Profiles found: {len(profiles)}")

            while True:
                if not profiles:
                    logging.info("No profiles found on this page, moving to the next page")
                    if self.scraper.is_next_button_disabled():
                        logging.info("Last page reached, stopping the bot")
                        break
                    else:
                        self.data_manager.update_last_page_visited(self.search_link, last_page_visited + 1)
                        return

                messages_sent = self.data_manager.count_messages_sent_today()
                logging.info(f"Messages sent today: {messages_sent}/{self.messages_per_day}")

                for profile in profiles:
                    if profile is None:
                        continue

                    if messages_sent >= self.messages_per_day:
                        logging.info(f"Daily message limit reached: {messages_sent}/{self.messages_per_day}")
                        return

                    logging.info(f"Visiting profile: {profile.get('linkedin_profile_link')}")
                    self.scraper.page.goto(profile.get('linkedin_profile_link'))
                    profile_details = self.scraper.scrape_profile_details()
                    if not profile_details:
                        logging.info(f"No profile details found for {profile.get('linkedin_profile_link')}")
                        continue

                    profile.update(profile_details)
                    self.scraper.click_connect_or_more_button()
                    next_message, self.message_toggle = get_next_message(self.message_a, self.message_b, self.message_toggle)
                    self.scraper.enter_custom_message(profile.get('first_name'), next_message)

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
                    logging.info(f"{messages_sent}/{self.messages_per_day} messages sent")

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
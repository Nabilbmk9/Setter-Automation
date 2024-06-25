import logging
from browser_manager import BrowserManager
from linkedin_scraper import LinkedInScraper
from data_manager import DataManager
from src.utils import extract_keywords_from_search_link, get_next_message
import threading
from gmail_api import run_email_checker


class MainController:
    def __init__(self, username, password, search_link, message_a, message_b, api_key, messages_per_day):
        self.browser_manager = None
        self.username = username
        self.password = password
        self.search_link = search_link
        self.message_a = message_a
        self.message_b = message_b
        self.api_key = api_key
        self.messages_per_day = messages_per_day
        self.scraper = None
        self.data_manager = DataManager(db_path='services/linkedin_contacts.db')
        self.message_toggle = False  # Pour alterner entre les messages

    def run(self):
        try:
            self.browser_manager = BrowserManager(headless=False, block_images=False)
            self.scraper = LinkedInScraper(self.browser_manager.new_page())

            email_thread = threading.Thread(target=run_email_checker, daemon=True)
            email_thread.start()

            self.scraper.login(self.username, self.password)
            self.scraper.ensure_authenticated()

            keywords = extract_keywords_from_search_link(self.search_link)
            self.data_manager.add_search_link(self.search_link, keywords)

            last_page_visited = self.data_manager.get_last_page_visited(self.search_link)
            self.scraper.page.goto(f"{self.search_link}&page={last_page_visited}")
            profiles = self.scraper.get_all_profiles_on_page()

            while True:
                if not profiles:
                    logging.info("Aucun profil trouvé sur cette page, passage à la page suivante")
                    if self.scraper.is_next_button_disabled():
                        logging.info("Dernière page atteinte, arrêt du bot")
                        break
                    else:
                        self.data_manager.update_last_page_visited(self.search_link, last_page_visited + 1)
                        return

                messages_sent = self.data_manager.count_messages_sent_today()

                for profile in profiles:
                    if profile is None:
                        continue

                    if messages_sent >= self.messages_per_day:
                        logging.info("Limite de messages par jour atteinte, arrêt du bot")
                        return

                    self.scraper.page.goto(profile.get('linkedin_profile_link'))
                    profile_details = self.scraper.scrape_profile_details()
                    if not profile_details:
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
                    logging.info(f"{messages_sent}/{self.messages_per_day} messages envoyés")

                if self.scraper.is_next_button_disabled():
                    logging.info("Dernière page atteinte, arrêt du bot")
                    break

                last_page_visited += 1
                self.data_manager.update_last_page_visited(self.search_link, last_page_visited)
                self.scraper.page.goto(f"{self.search_link}&page={last_page_visited}")
                profiles = self.scraper.get_all_profiles_on_page()

        except Exception as e:
            logging.error(f"Erreur lors de l'exécution du bot : {e}")
        finally:
            if self.browser_manager:
                self.browser_manager.close()

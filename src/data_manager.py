import sqlite3
from datetime import datetime, date
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataManager:
    def __init__(self, db_path='linkedin_contacts.db'):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
        logger.info("Base de données initialisée avec succès")

    def _create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    first_name TEXT,
                    last_name TEXT,
                    linkedin_profile_link TEXT NOT NULL UNIQUE,
                    date_contacted TEXT,
                    notes TEXT
                );
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS search_links (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    search_link TEXT NOT NULL UNIQUE,
                    last_page_visited INTEGER DEFAULT 1,
                    date_last_visited TEXT,
                    keyword TEXT
                );
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_template TEXT,
                    response_received BOOLEAN,
                    date_sent TEXT,
                    contact_id INTEGER,
                    search_id INTEGER,
                    FOREIGN KEY(contact_id) REFERENCES contacts(id),
                    FOREIGN KEY(search_id) REFERENCES search_links(id)
                );
            ''')
            self.conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_contacts_linkedin_profile_link
                ON contacts (linkedin_profile_link);
            ''')
            self.conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_search_links_search_link
                ON search_links (search_link);
            ''')
        logger.info("Tables créées ou vérifiées avec succès")

    def add_contact(self, full_name, first_name, last_name, linkedin_profile_link, notes=""):
        with self.conn:
            self.conn.execute('''
                INSERT OR IGNORE INTO contacts (full_name, first_name, last_name, linkedin_profile_link, date_contacted, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (full_name, first_name, last_name, linkedin_profile_link, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), notes))
        logger.info(f"Contact ajouté ou existant ignoré: {full_name} ({linkedin_profile_link})")

    def update_contact(self, linkedin_profile_link, notes):
        with self.conn:
            self.conn.execute('''
                UPDATE contacts
                SET notes = ?, date_contacted = ?
                WHERE linkedin_profile_link = ?
            ''', (notes, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), linkedin_profile_link))
        logger.info(f"Contact mis à jour: {linkedin_profile_link}")

    def add_search_link(self, search_link, keyword):
        with self.conn:
            self.conn.execute('''
                INSERT OR IGNORE INTO search_links (search_link, keyword, date_last_visited)
                VALUES (?, ?, ?)
            ''', (search_link, keyword, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        logger.info(f"Lien de recherche ajouté ou existant ignoré: {search_link}")

    def update_last_page_visited(self, search_link, last_page_visited):
        with self.conn:
            self.conn.execute('''
                UPDATE search_links
                SET last_page_visited = ?, date_last_visited = ?
                WHERE search_link = ?
            ''', (last_page_visited, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), search_link))
        logger.info(f"Dernière page visitée mise à jour pour le lien de recherche: {search_link}")

    def get_last_page_visited(self, search_link):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT last_page_visited FROM search_links WHERE search_link = ?
        ''', (search_link,))
        result = cursor.fetchone()
        last_page = result[0] if result else 1
        logger.info(f"Dernière page visitée récupérée pour le lien de recherche {search_link}: {last_page}")
        return last_page

    def add_message(self, message_template, contact_id, search_id, response_received=False):
        with self.conn:
            self.conn.execute('''
                INSERT INTO messages (message_template, response_received, date_sent, contact_id, search_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (message_template, response_received, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), contact_id, search_id))
        logger.info(f"Message ajouté pour le contact ID {contact_id} et recherche ID {search_id}")

    def update_message_response(self, message_id, response_received):
        with self.conn:
            self.conn.execute('''
                UPDATE messages
                SET response_received = ?
                WHERE id = ?
            ''', (response_received, message_id))
        logger.info(f"Réponse du message mise à jour pour le message ID {message_id}")

    def get_contact_id(self, linkedin_profile_link):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id FROM contacts WHERE linkedin_profile_link = ?
        ''', (linkedin_profile_link,))
        result = cursor.fetchone()
        contact_id = result[0] if result else None
        logger.info(f"ID du contact récupéré pour le lien de profil {linkedin_profile_link}: {contact_id}")
        return contact_id

    def get_search_id(self, search_link):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id FROM search_links WHERE search_link = ?
        ''', (search_link,))
        result = cursor.fetchone()
        search_id = result[0] if result else None
        logger.info(f"ID de la recherche récupéré pour le lien de recherche {search_link}: {search_id}")
        return search_id

    def count_messages_sent_today(self):
        cursor = self.conn.cursor()
        today = date.today().strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT COUNT(*) FROM messages WHERE date(date_sent) = ?
        ''', (today,))
        result = cursor.fetchone()
        messages_sent_today = result[0] if result else 0
        logger.info(f"Nombre de messages envoyés aujourd'hui : {messages_sent_today}")
        return messages_sent_today

    def check_full_name_exists(self, full_name):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT 1 FROM contacts
        WHERE full_name = ?
        """, (full_name,))
        return cursor.fetchone() is not None

    def mark_message_as_responded(self, full_name):
        cursor = self.conn.cursor()
        # Récupérer l'ID du contact à partir du nom complet
        cursor.execute('''
            SELECT id FROM contacts WHERE full_name = ?
        ''', (full_name,))
        contact = cursor.fetchone()

        if contact:
            contact_id = contact[0]
            with self.conn:
                self.conn.execute('''
                    UPDATE messages
                    SET response_received = 1
                    WHERE contact_id = ?
                ''', (contact_id,))
                self.conn.commit()
                logger.info(f"Réponse détectée et enregistrée pour le contact ID : {contact_id} ({full_name})")
        else:
            logger.info(f"Aucune correspondance trouvée pour : {full_name}")

import sys
import logging
import sqlite3
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.announcement_window import AnnouncementWindow
from ui.styles import get_stylesheet
from utils.requests_handler import fetch_announcement, check_for_updates


def main():
    # Configurer la journalisation pour écrire dans un fichier
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log',
                        filemode='w')

    logging.debug("Application started")

    # Test de l'importation de sqlite3
    try:
        logging.debug("Testing sqlite3 import and connection...")
        conn = sqlite3.connect(':memory:')
        logging.debug("Successfully connected to sqlite3 in-memory database.")
        conn.close()
    except Exception as e:
        logging.error(f"Error during sqlite3 test: {e}")
        raise

    try:
        app = QApplication([])

        # Appliquer le style globalement
        app.setStyleSheet(get_stylesheet())
        logging.debug("Stylesheet applied")

        # Vérifier les mises à jour
        current_version = "1.0.0"  # Remplacez par votre version actuelle
        has_update, latest_version = check_for_updates(current_version)
        logging.debug(f"Update check completed: has_update={has_update}, latest_version={latest_version}")

        # Récupérer l'annonce dynamique
        announcement_message = fetch_announcement()
        logging.debug(f"Fetched announcement: {announcement_message}")

        # Construire le message combiné
        combined_message = ""
        if announcement_message and has_update:
            combined_message = f"{announcement_message}<br><br>Une nouvelle version ({latest_version}) est disponible !"
        elif announcement_message:
            combined_message = announcement_message
        elif has_update:
            combined_message = f"Une nouvelle version ({latest_version}) est disponible !"

        logging.debug(f"Combined message: {combined_message}")

        # Créer la fenêtre principale
        main_window = MainWindow()
        logging.debug("Main window created")

        # Afficher la fenêtre d'annonces si nécessaire
        if combined_message:
            announcement_window = AnnouncementWindow(combined_message, parent=main_window)
            logging.debug("Announcement window created")
            announcement_window.exec()
            logging.debug("Announcement window executed")

        # Afficher la fenêtre principale
        main_window.show()
        logging.debug("Main window shown")

        sys.exit(app.exec())
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise


if __name__ == '__main__':
    main()

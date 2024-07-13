import sys
import logging
import sqlite3
import json
import os
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.announcement_window import AnnouncementWindow
from ui.styles import get_stylesheet
from utils.requests_handler import fetch_announcement, check_for_updates
from config.logging_config import setup_logging


def get_resource_path(relative_path):
    """Obtenir le chemin absolu d'une ressource, en utilisant `sys._MEIPASS` si disponible."""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def load_config(file_path):
    # Chemin local et chemin empaqueté
    local_full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_path)
    packaged_full_path = get_resource_path(f"_internal/{file_path}")

    # Log the paths for debugging
    logging.debug(f"Local full path: {local_full_path}")
    logging.debug(f"Packaged full path: {packaged_full_path}")

    # Vérifier l'existence du fichier dans les deux emplacements
    if os.path.exists(local_full_path):
        full_path = local_full_path
        logging.debug(f"Config file found at local path: {local_full_path}")
    elif os.path.exists(packaged_full_path):
        full_path = packaged_full_path
        logging.debug(f"Config file found at packaged path: {packaged_full_path}")
    else:
        logging.error(f"Config file does not exist in either path: {local_full_path} or {packaged_full_path}")
        raise FileNotFoundError(f"No such file or directory: '{local_full_path}' or '{packaged_full_path}'")

    with open(full_path, 'r') as f:
        return json.load(f)


def main():
    # Configurer la journalisation pour écrire dans un fichier ou dans le terminal
    logger = setup_logging()
    logger.debug("Application started")

    logger.debug(f"Current working directory: {os.getcwd()}")

    # Charger les configurations
    try:
        user_config = load_config('config/user_config.json')
        app_config = load_config('config/app_config.json')
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        return

    current_version = app_config['current_version']
    update_url = app_config['update_url']
    announcement_url = app_config['announcement_url']
    version_url = app_config['version_url']

    # Test de l'importation de sqlite3
    try:
        logger.debug("Testing sqlite3 import and connection...")
        conn = sqlite3.connect(':memory:')
        logger.debug("Successfully connected to sqlite3 in-memory database.")
        conn.close()
    except Exception as e:
        logger.error(f"Error during sqlite3 test: {e}")
        raise

    try:
        app = QApplication([])

        # Appliquer le style globalement
        app.setStyleSheet(get_stylesheet())
        logger.debug("Stylesheet applied")

        # Vérifier les mises à jour
        has_update, latest_version = check_for_updates(current_version, version_url)
        logger.debug(f"Update check completed: has_update={has_update}, latest_version={latest_version}")

        # Récupérer l'annonce dynamique
        announcement_message = fetch_announcement(announcement_url)
        logger.debug(f"Fetched announcement: {announcement_message}")

        # Construire le message combiné
        combined_message = ""
        if announcement_message and has_update:
            combined_message = f"{announcement_message}<br><br>Une nouvelle version ({latest_version}) est disponible !"
        elif announcement_message:
            combined_message = announcement_message
        elif has_update:
            combined_message = f"Une nouvelle version ({latest_version}) est disponible !"

        logger.debug(f"Combined message: {combined_message}")

        # Créer la fenêtre principale
        main_window = MainWindow()
        logger.debug("Main window created")

        # Afficher la fenêtre d'annonces si nécessaire
        if combined_message:
            announcement_window = AnnouncementWindow(combined_message, update_url if has_update else None,
                                                     parent=main_window)
            logger.debug("Announcement window created")
            announcement_window.exec()
            logger.debug("Announcement window executed")

        # Afficher la fenêtre principale
        main_window.show()
        logger.debug("Main window shown")

        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise


if __name__ == '__main__':
    main()

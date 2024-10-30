# main.py

import sys
import logging
import os
import json
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox
from config.logging_config import setup_logging
from config.config import load_config, update_config
from utils.requests_handler import fetch_announcement, check_for_updates
from utils.license_utils import verify_license
from ui.announcement_window import AnnouncementWindow
from ui.license_window import LicenseWindow
from ui.styles import get_stylesheet
from utils.utils import get_resource_path


def load_app_config(file_path):
    """Charge la configuration de l'application depuis un fichier JSON."""
    # Chemin local et chemin empaqueté
    local_full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_path)
    packaged_full_path = get_resource_path(f"_internal/{file_path}")

    # Log des chemins pour le débogage
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
    # Configurer la journalisation
    logger = setup_logging()
    logger.debug("Application démarrée")

    # Charger la configuration utilisateur
    try:
        user_config = load_config()
    except Exception as e:
        logger.error(f"Erreur lors du chargement de la configuration utilisateur: {e}")
        return

    app = QApplication([])

    # Appliquer le style
    app.setStyleSheet(get_stylesheet())
    logger.debug("Stylesheet appliqué")

    # Charger les configurations de l'application
    try:
        app_config = load_app_config('config/app_config.json')
    except Exception as e:
        logger.error(f"Erreur lors du chargement de la configuration de l'application: {e}")
        return

    # Valider la présence des clés nécessaires
    required_keys = ['current_version', 'update_url', 'announcement_url', 'version_url']
    for key in required_keys:
        if key not in app_config:
            logger.error(f"La clé '{key}' est manquante dans app_config.json.")
            return

    current_version = app_config['current_version']
    update_url = app_config['update_url']
    announcement_url = app_config['announcement_url']
    version_url = app_config['version_url']

    # Vérifier les mises à jour
    has_update, latest_version = check_for_updates(current_version, version_url)
    logger.debug(f"Vérification des mises à jour terminée: has_update={has_update}, latest_version={latest_version}")

    # Récupérer l'annonce dynamique
    announcement_message = fetch_announcement(announcement_url)
    logger.debug(f"Annonce récupérée: {announcement_message}")

    # Construire le message combiné
    combined_message = ""
    if announcement_message and has_update:
        combined_message = f"{announcement_message}<br><br>Une nouvelle version ({latest_version}) est disponible !"
    elif announcement_message:
        combined_message = announcement_message
    elif has_update:
        combined_message = f"Une nouvelle version ({latest_version}) est disponible !"

    logger.debug(f"Message combiné: {combined_message}")

    # Vérifier la licence
    license_key = user_config.get('LICENSE_KEY', '')
    valid, license_type = verify_license(license_key)
    if not valid:
        # Demander la saisie de la licence si invalide
        license_window = LicenseWindow()
        if license_window.exec() != QDialog.Accepted:
            sys.exit()  # Quitter l'application si la licence n'est pas validée
        else:
            # Recharger la configuration pour obtenir la nouvelle clé de licence
            user_config = load_config()
            license_key = user_config.get('LICENSE_KEY', '')
            valid, license_type = verify_license(license_key)
            if not valid:
                QMessageBox.critical(None, "Erreur de licence", "Licence invalide ou expirée.")
                sys.exit()

    # Enregistrer le type de licence dans la configuration
    user_config['LICENSE_TYPE'] = license_type
    update_config(user_config)
    logger.debug(f"Type de licence : {license_type}")

    # Importer la classe appropriée pour la fenêtre principale en fonction du type de licence
    if license_type == 'ultimate':
        from ui.ultimate_main_window import UltimateMainWindow as MainWindowClass
        logger.debug("Licence ultimate détectée, chargement de UltimateMainWindow")
    elif license_type == 'premium':
        from ui.premium_main_window import PremiumMainWindow as MainWindowClass
        logger.debug("Licence premium détectée, chargement de PremiumMainWindow")
    else:
        from ui.standard_main_window import StandardMainWindow as MainWindowClass
        logger.debug("Licence standard détectée, chargement de StandardMainWindow")

    # Créer la fenêtre principale
    main_window = MainWindowClass()
    logger.debug("Fenêtre principale créée")

    # Afficher la fenêtre d'annonces si nécessaire
    if combined_message:
        announcement_window = AnnouncementWindow(combined_message, update_url if has_update else None,
                                                 parent=main_window)
        logger.debug("Fenêtre d'annonce créée")
        announcement_window.exec()
        logger.debug("Fenêtre d'annonce exécutée")

    # Afficher la fenêtre principale
    main_window.show()
    logger.debug("Fenêtre principale affichée")

    sys.exit(app.exec())


if __name__ == '__main__':
    main()

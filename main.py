import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.announcement_window import AnnouncementWindow
from ui.styles import get_stylesheet
from utils.requests_handler import fetch_announcement, check_for_updates


def main():
    app = QApplication([])

    # Appliquer le style globalement
    app.setStyleSheet(get_stylesheet())

    # Vérifier les mises à jour
    current_version = "1.0.0"  # Remplacez par votre version actuelle
    has_update, latest_version = check_for_updates(current_version)

    # Récupérer l'annonce dynamique
    announcement_message = fetch_announcement()

    # Construire le message combiné
    combined_message = ""
    if announcement_message and has_update:
        combined_message = f"{announcement_message}<br><br>Une nouvelle version ({latest_version}) est disponible !"
    elif announcement_message:
        combined_message = announcement_message
    elif has_update:
        combined_message = f"Une nouvelle version ({latest_version}) est disponible !"

    # Créer la fenêtre principale
    main_window = MainWindow()

    # Afficher la fenêtre d'annonces si nécessaire
    if combined_message:
        announcement_window = AnnouncementWindow(combined_message, parent=main_window)
        announcement_window.exec()

    # Afficher la fenêtre principale
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

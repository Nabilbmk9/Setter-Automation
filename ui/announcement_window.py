import os
import requests
import logging
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from ui.styles import get_stylesheet


class AnnouncementWindow(QDialog):
    def __init__(self, message, update_url=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Annonce")
        self.setStyleSheet(get_stylesheet())
        self.setMinimumSize(400, 300)

        self.update_url = update_url

        layout = QVBoxLayout()

        self.message_label = QLabel()
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)
        self.message_label.setTextFormat(Qt.RichText)
        self.message_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.message_label.setOpenExternalLinks(True)
        self.message_label.setText(message)
        layout.addWidget(self.message_label)

        if self.update_url:
            update_button = QPushButton("Mettre à jour")
            update_button.clicked.connect(self.download_update)
            layout.addWidget(update_button)

        close_button = QPushButton("Fermer")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def download_update(self):
        try:
            response = requests.get(self.update_url, stream=True)
            response.raise_for_status()
            update_path = os.path.join(os.getenv('APPDATA'), 'latest_update.exe')
            with open(update_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            QMessageBox.information(self, "Téléchargement terminé",
                                    "La mise à jour a été téléchargée. L'installation va commencer.")
            os.startfile(update_path)
            self.accept()
        except Exception as e:
            logging.error(f"Failed to download update: {e}")
            QMessageBox.critical(self, "Erreur", "Le téléchargement de la mise à jour a échoué.")

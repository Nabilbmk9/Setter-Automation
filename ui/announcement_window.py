import os
import requests
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox, QProgressBar
from PySide6.QtCore import Qt, QThread, Signal
from ui.styles import get_stylesheet
from config.logging_config import setup_logging

logger = setup_logging()


class DownloadThread(QThread):
    progress = Signal(int)
    finished = Signal()

    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path

    def run(self):
        try:
            response = requests.get(self.url, stream=True)
            response.raise_for_status()
            total_length = response.headers.get('content-length')

            with open(self.save_path, 'wb') as f:
                if total_length is None:  # no content length header
                    f.write(response.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            dl += len(chunk)
                            f.write(chunk)
                            done = int(50 * dl / total_length)
                            self.progress.emit(done)
            self.finished.emit()
        except Exception as e:
            logger.error(f"Failed to download update: {e}")
            self.finished.emit()


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
            self.update_button = QPushButton("Mettre à jour")
            self.update_button.clicked.connect(self.download_update)
            layout.addWidget(self.update_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        close_button = QPushButton("Fermer")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def download_update(self):
        self.progress_bar.setVisible(True)
        self.status_label.setText("Téléchargement en cours...")
        update_path = os.path.join(os.getenv('APPDATA'), 'latest_update.exe')
        self.download_thread = DownloadThread(self.update_url, update_path)
        self.download_thread.progress.connect(self.progress_bar.setValue)
        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.start()

    def on_download_finished(self):
        self.progress_bar.setVisible(False)
        self.status_label.setText("Téléchargement terminé. Installation en cours...")
        update_path = os.path.join(os.getenv('APPDATA'), 'latest_update.exe')
        try:
            os.startfile(update_path)
            self.accept()
        except Exception as e:
            logger.error(f"Failed to start update: {e}")
            QMessageBox.critical(self, "Erreur", "L'installation de la mise à jour a échoué.")

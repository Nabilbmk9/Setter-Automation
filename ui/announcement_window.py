from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt


class AnnouncementWindow(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Annonces et Mises à Jour")
        self.resize(400, 200)

        layout = QVBoxLayout()

        # Message d'annonce
        self.message_label = QLabel()
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)  # Permet de gérer les longs textes
        self.message_label.setTextFormat(Qt.RichText)
        self.message_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.message_label.setOpenExternalLinks(True)
        self.message_label.setText(message)
        layout.addWidget(self.message_label)

        # Bouton de fermeture
        self.close_button = QPushButton("Fermer")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

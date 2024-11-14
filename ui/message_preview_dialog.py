# message_preview_dialog.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt


class MessagePreviewDialog(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Prévisualisation du message")
        self.message = message
        # Ajouter le drapeau pour que la fenêtre reste au-dessus
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        message_label = QLabel("Voici le message généré :")
        layout.addWidget(message_label)

        self.message_text_edit = QTextEdit()
        self.message_text_edit.setText(self.message)
        self.message_text_edit.setReadOnly(True)
        layout.addWidget(self.message_text_edit)

        # Boutons
        buttons_layout = QHBoxLayout()

        self.accept_button = QPushButton("Accepter")
        self.retry_button = QPushButton("Ressayer")
        self.cancel_button = QPushButton("Annuler")

        buttons_layout.addWidget(self.accept_button)
        buttons_layout.addWidget(self.retry_button)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Connecter les boutons
        self.accept_button.clicked.connect(self.accept)
        self.retry_button.clicked.connect(self.retry)
        self.cancel_button.clicked.connect(self.reject)

        # Assurer que la fenêtre prend le focus
        self.raise_()
        self.activateWindow()

    def retry(self):
        # Retourne un code spécifique pour indiquer le choix de "Ressayer"
        self.done(2)

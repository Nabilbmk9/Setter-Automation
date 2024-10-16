# standard_main_window.py
from PySide6.QtCore import Qt

from ui.base_main_window import BaseMainWindow
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton

class StandardMainWindow(BaseMainWindow):
    def __init__(self):
        super().__init__()

    def setup_ui(self):
        """Configure l'interface utilisateur pour la licence standard."""
        # Titre de l'application
        self.title_label = QLabel("Bot LinkedIn")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("title")
        self.title_label.setFont(self.font)
        self.layout.addWidget(self.title_label)
        self.layout.addSpacing(30)

        # Champs de saisie pour l'email LinkedIn
        self.username_label = QLabel("Email LinkedIn:")
        self.username_label.setFont(self.font)
        self.username_input = QLineEdit(self.config.get('LINKEDIN_EMAIL', ''))
        self.username_input.setFont(self.font)
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)

        # Champs de saisie pour le mot de passe LinkedIn
        self.password_label = QLabel("Mot de passe LinkedIn:")
        self.password_label.setFont(self.font)
        self.password_input = QLineEdit(self.config.get('LINKEDIN_PASSWORD', ''))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(self.font)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)

        # Champs de saisie pour le lien de recherche
        self.search_link_label = QLabel("Lien de recherche:")
        self.search_link_label.setFont(self.font)
        self.search_link_input = QLineEdit(self.config.get('LINKEDIN_SEARCH_LINK', ''))
        self.search_link_input.setFont(self.font)
        self.layout.addWidget(self.search_link_label)
        self.layout.addWidget(self.search_link_input)

        # Initialiser les messages A et B
        self.message_a_text = self.config.get('MESSAGE_A', '')
        self.message_b_text = self.config.get('MESSAGE_B', '')

        # Section pour le Message Template A
        self.message_a_label = QLabel("Message Template A:")
        self.message_a_label.setFont(self.font)
        self.layout.addWidget(self.message_a_label)

        self.message_a_button = QPushButton(self.get_message_preview(self.message_a_text))
        self.message_a_button.setFont(self.font)
        self.message_a_button.setObjectName("messageButton")
        self.message_a_button.clicked.connect(self.edit_message_a)
        self.layout.addWidget(self.message_a_button)

        # Section pour le Message Template B
        self.message_b_label = QLabel("Message Template B:")
        self.message_b_label.setFont(self.font)
        self.layout.addWidget(self.message_b_label)

        self.message_b_button = QPushButton(self.get_message_preview(self.message_b_text))
        self.message_b_button.setFont(self.font)
        self.message_b_button.setObjectName("messageButton")
        self.message_b_button.clicked.connect(self.edit_message_b)
        self.layout.addWidget(self.message_b_button)

        # Champs de saisie pour le nombre de messages par jour
        self.messages_per_day_label = QLabel("Messages par jour:")
        self.messages_per_day_label.setFont(self.font)
        self.messages_per_day_input = QLineEdit(str(self.config.get('MESSAGES_PER_DAY', '10')))
        self.messages_per_day_input.setFont(self.font)
        self.layout.addWidget(self.messages_per_day_label)
        self.layout.addWidget(self.messages_per_day_input)

        # Bouton pour démarrer le bot
        self.start_button = QPushButton("Start Bot")
        self.start_button.setFont(self.font)
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self.start_bot)
        self.layout.addWidget(self.start_button)

    def get_message_preview(self, message):
        """Retourne un aperçu du message (50 premiers caractères)."""
        if message:
            preview = message[:50] + '...' if len(message) > 50 else message
        else:
            preview = "Message vide, cliquez pour remplir"
        return preview

    def edit_message_a(self):
        """Ouvre une boîte de dialogue pour éditer le Message Template A."""
        dialog = MessageEditDialog("Éditer Message Template A", self.message_a_text)
        if dialog.exec():
            self.message_a_text = dialog.get_text()
            self.message_a_button.setText(self.get_message_preview(self.message_a_text))

    def edit_message_b(self):
        """Ouvre une boîte de dialogue pour éditer le Message Template B."""
        dialog = MessageEditDialog("Éditer Message Template B", self.message_b_text)
        if dialog.exec():
            self.message_b_text = dialog.get_text()
            self.message_b_button.setText(self.get_message_preview(self.message_b_text))

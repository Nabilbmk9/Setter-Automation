from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QFont
from controllers.main_controller import MainController
from config.config import load_config, update_config
from ui.styles import get_stylesheet

import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bot Application")
        self.resize(400, 600)  # Changer la taille de la fenêtre (largeur, hauteur)

        # Charger la configuration
        self.config = load_config()

        # Débogage du chemin du fichier de police
        font_path = os.path.abspath('ui/fonts/Montserrat-Regular.ttf')

        # Charger les polices Montserrat
        font_id = QFontDatabase.addApplicationFont(font_path)
        loaded_fonts = QFontDatabase.applicationFontFamilies(font_id)

        # Définir la police Montserrat pour les widgets
        montserrat = QFont("Montserrat", 10)

        # Appliquer le style
        self.setStyleSheet(get_stylesheet())

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.title_label = QLabel("Titre de l'Application")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("title")
        self.title_label.setFont(montserrat)
        layout.addWidget(self.title_label)
        layout.addSpacing(30)  # Ajouter plus d'espace sous le titre

        self.username_label = QLabel("Email LinkedIn:")
        self.username_label.setFont(montserrat)
        self.username_input = QLineEdit(self.config.get('LINKEDIN_EMAIL', ''))
        self.username_input.setFont(montserrat)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Mot de passe LinkedIn:")
        self.password_label.setFont(montserrat)
        self.password_input = QLineEdit(self.config.get('LINKEDIN_PASSWORD', ''))
        self.password_input.setEchoMode(QLineEdit.Password)  # Masquer le texte du mot de passe
        self.password_input.setFont(montserrat)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.search_link_label = QLabel("Lien de recherche:")
        self.search_link_label.setFont(montserrat)
        self.search_link_input = QLineEdit(self.config.get('LINKEDIN_SEARCH_LINK', ''))
        self.search_link_input.setFont(montserrat)
        layout.addWidget(self.search_link_label)
        layout.addWidget(self.search_link_input)

        self.message_a_label = QLabel("Message Template A:")
        self.message_a_label.setFont(montserrat)
        self.message_a_input = QLineEdit(self.config.get('MESSAGE_A', ''))
        self.message_a_input.setFont(montserrat)
        layout.addWidget(self.message_a_label)
        layout.addWidget(self.message_a_input)

        self.message_b_label = QLabel("Message Template B:")
        self.message_b_label.setFont(montserrat)
        self.message_b_input = QLineEdit(self.config.get('MESSAGE_B', ''))
        self.message_b_input.setFont(montserrat)
        layout.addWidget(self.message_b_label)
        layout.addWidget(self.message_b_input)

        self.messages_per_day_label = QLabel("Messages Per Day:")
        self.messages_per_day_label.setFont(montserrat)
        self.messages_per_day_input = QLineEdit(self.config.get('MESSAGES_PER_DAY', '10'))
        self.messages_per_day_input.setFont(montserrat)
        layout.addWidget(self.messages_per_day_label)
        layout.addWidget(self.messages_per_day_input)

        self.start_button = QPushButton("Start Bot")
        self.start_button.setFont(montserrat)
        self.start_button.clicked.connect(self.start_bot)
        layout.addWidget(self.start_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_bot(self):
        username = self.username_input.text()
        password = self.password_input.text()
        search_link = self.search_link_input.text()
        message_a = self.message_a_input.text()
        message_b = self.message_b_input.text()
        messages_per_day = self.messages_per_day_input.text()

        if not all([username, password, search_link, message_a, message_b, messages_per_day]):
            QMessageBox.warning(self, "Input Error", "All fields must be filled!")
            return

        # Sauvegarder les nouvelles valeurs dans le fichier .env
        self.config.update({
            'LINKEDIN_EMAIL': username,
            'LINKEDIN_PASSWORD': password,
            'LINKEDIN_SEARCH_LINK': search_link,
            'MESSAGE_A': message_a,
            'MESSAGE_B': message_b,
            'MESSAGES_PER_DAY': messages_per_day
        })
        update_config(self.config)

        self.controller = MainController(
            username=username,
            password=password,
            search_link=search_link,
            message_a=message_a,
            message_b=message_b,
            messages_per_day=int(messages_per_day)
        )

        self.controller.run()
        QMessageBox.information(self, "Bot Started", "The bot has been started.")

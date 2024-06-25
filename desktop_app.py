import sys
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QMessageBox
from PySide6.QtGui import QFontDatabase, QFont
from main_controller import MainController
from dotenv import load_dotenv, set_key, find_dotenv

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bot Application")
        self.resize(400, 600)  # Changer la taille de la fenêtre (largeur, hauteur)

        # Charger les valeurs du fichier .env
        load_dotenv()
        self.env_path = find_dotenv()

        # Charger les polices Montserrat
        font_id_1 = QFontDatabase.addApplicationFont('ui/fonts/Montserrat-Regular.ttf')
        font_id_2 = QFontDatabase.addApplicationFont('ui/fonts/Montserrat-Bold.ttf')

        # Définir les polices pour les widgets
        montserrat_regular = QFont("Montserrat", 10)

        # Appliquer le style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0c1021;
            }
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QLabel#title {
                font-size: 24px;
                margin-bottom: 20px;
            }
            QLineEdit {
                background-color: #243672;
                color: white;
                border: 2px solid #7a3ef3;
                border-radius: 10px;
                padding: 5px;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #ff4500;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #ff5714;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.title_label = QLabel("Titre de l'Application")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("title")
        self.title_label.setFont(montserrat_regular)
        layout.addWidget(self.title_label)
        layout.addSpacing(30)  # Ajouter plus d'espace sous le titre

        self.username_label = QLabel("Email LinkedIn:")
        self.username_label.setFont(montserrat_regular)
        self.username_input = QLineEdit(os.getenv('LINKEDIN_EMAIL', ''))
        self.username_input.setFont(montserrat_regular)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Mot de passe LinkedIn:")
        self.password_label.setFont(montserrat_regular)
        self.password_input = QLineEdit(os.getenv('LINKEDIN_PASSWORD', ''))
        self.password_input.setEchoMode(QLineEdit.Password)  # Masquer le texte du mot de passe
        self.password_input.setFont(montserrat_regular)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.search_link_label = QLabel("Lien de recherche:")
        self.search_link_label.setFont(montserrat_regular)
        self.search_link_input = QLineEdit(os.getenv('LINKEDIN_SEARCH_LINK', ''))
        self.search_link_input.setFont(montserrat_regular)
        layout.addWidget(self.search_link_label)
        layout.addWidget(self.search_link_input)

        self.message_a_label = QLabel("Message Template A:")
        self.message_a_label.setFont(montserrat_regular)
        self.message_a_input = QLineEdit(os.getenv('MESSAGE_A', ''))
        self.message_a_input.setFont(montserrat_regular)
        layout.addWidget(self.message_a_label)
        layout.addWidget(self.message_a_input)

        self.message_b_label = QLabel("Message Template B:")
        self.message_b_label.setFont(montserrat_regular)
        self.message_b_input = QLineEdit(os.getenv('MESSAGE_B', ''))
        self.message_b_input.setFont(montserrat_regular)
        layout.addWidget(self.message_b_label)
        layout.addWidget(self.message_b_input)

        self.api_key_label = QLabel("OpenAI API Key:")
        self.api_key_label.setFont(montserrat_regular)
        self.api_key_input = QLineEdit(os.getenv('GPT_API_KEY', ''))
        self.api_key_input.setEchoMode(QLineEdit.Password)  # Masquer le texte de la clé API
        self.api_key_input.setFont(montserrat_regular)
        layout.addWidget(self.api_key_label)
        layout.addWidget(self.api_key_input)

        self.messages_per_day_label = QLabel("Messages Per Day:")
        self.messages_per_day_label.setFont(montserrat_regular)
        self.messages_per_day_input = QLineEdit(os.getenv('MESSAGES_PER_DAY', '10'))
        self.messages_per_day_input.setFont(montserrat_regular)
        layout.addWidget(self.messages_per_day_label)
        layout.addWidget(self.messages_per_day_input)

        self.start_button = QPushButton("Start Bot")
        self.start_button.setFont(montserrat_regular)
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
        api_key = self.api_key_input.text()
        messages_per_day = self.messages_per_day_input.text()

        if not all([username, password, search_link, message_a, message_b, api_key, messages_per_day]):
            QMessageBox.warning(self, "Input Error", "All fields must be filled!")
            return

        # Sauvegarder les nouvelles valeurs dans le fichier .env
        self.update_env_file('LINKEDIN_EMAIL', username)
        self.update_env_file('LINKEDIN_PASSWORD', password)
        self.update_env_file('LINKEDIN_SEARCH_LINK', search_link)
        self.update_env_file('MESSAGE_A', message_a)
        self.update_env_file('MESSAGE_B', message_b)
        self.update_env_file('GPT_API_KEY', api_key)
        self.update_env_file('MESSAGES_PER_DAY', messages_per_day)

        self.controller = MainController(
            username=username,
            password=password,
            search_link=search_link,
            message_a=message_a,
            message_b=message_b,
            api_key=api_key,
            messages_per_day=int(messages_per_day)
        )

        self.controller.run()
        QMessageBox.information(self, "Bot Started", "The bot has been started.")

    def update_env_file(self, key, value):
        set_key(self.env_path, key, value)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

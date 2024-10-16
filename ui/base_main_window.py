# base_main_window.py

import logging
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton,
    QMessageBox
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt

from config.config import load_config, update_config
from controllers.main_controller import MainController
from ui.styles import get_stylesheet
from utils.utils import get_resource_path
from ui.message_edit_dialog import MessageEditDialog


class BaseMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bot LinkedIn")
        self.setWindowIcon(QIcon(get_resource_path("ui/resources/logo3d.png")))
        self.resize(400, 600)

        # Initialiser la configuration et la police
        self.config = load_config()
        self.font = QFont("Montserrat", 10)
        self.setStyleSheet(get_stylesheet())

        # Créer le layout principal
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)

        # Configurer les composants de l'UI
        self.setup_ui()

        # Définir le widget central
        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

    def setup_ui(self):
        """Configure l'interface utilisateur en appelant des méthodes de configuration spécifiques."""
        self.setup_title()
        self.setup_linkedin_credentials()
        self.setup_search_link()
        self.setup_message_templates()
        self.setup_messages_per_day()
        self.setup_start_button()

    def setup_title(self):
        """Configure le titre de l'application."""
        self.title_label = QLabel("Bot LinkedIn")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("title")
        self.title_label.setFont(self.font)
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addSpacing(30)

    def setup_linkedin_credentials(self):
        """Configure les champs pour l'email et le mot de passe LinkedIn."""
        # Email
        self.username_label = QLabel("Email LinkedIn:")
        self.username_label.setFont(self.font)
        self.username_input = QLineEdit(self.config.get('LINKEDIN_EMAIL', ''))
        self.username_input.setFont(self.font)
        self.main_layout.addWidget(self.username_label)
        self.main_layout.addWidget(self.username_input)

        # Mot de passe
        self.password_label = QLabel("Mot de passe LinkedIn:")
        self.password_label.setFont(self.font)
        self.password_input = QLineEdit(self.config.get('LINKEDIN_PASSWORD', ''))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(self.font)
        self.main_layout.addWidget(self.password_label)
        self.main_layout.addWidget(self.password_input)

    def setup_search_link(self):
        """Configure le champ pour le lien de recherche."""
        self.search_link_label = QLabel("Lien de recherche:")
        self.search_link_label.setFont(self.font)
        self.search_link_input = QLineEdit(self.config.get('LINKEDIN_SEARCH_LINK', ''))
        self.search_link_input.setFont(self.font)
        self.main_layout.addWidget(self.search_link_label)
        self.main_layout.addWidget(self.search_link_input)

    def setup_message_templates(self):
        """Configure les templates des messages A et B."""
        self.message_a_text = self.config.get('MESSAGE_A', '')
        self.message_b_text = self.config.get('MESSAGE_B', '')

        # Message A
        self.message_a_label = QLabel("Message Template A:")
        self.message_a_label.setFont(self.font)
        self.main_layout.addWidget(self.message_a_label)

        self.message_a_button = QPushButton(self.get_message_preview(self.message_a_text))
        self.message_a_button.setFont(self.font)
        self.message_a_button.setObjectName("messageButton")
        self.message_a_button.clicked.connect(self.edit_message_a)
        self.main_layout.addWidget(self.message_a_button)

        # Message B
        self.message_b_label = QLabel("Message Template B:")
        self.message_b_label.setFont(self.font)
        self.main_layout.addWidget(self.message_b_label)

        self.message_b_button = QPushButton(self.get_message_preview(self.message_b_text))
        self.message_b_button.setFont(self.font)
        self.message_b_button.setObjectName("messageButton")
        self.message_b_button.clicked.connect(self.edit_message_b)
        self.main_layout.addWidget(self.message_b_button)

    def setup_messages_per_day(self):
        """Configure le champ pour le nombre de messages par jour."""
        self.messages_per_day_label = QLabel("Messages par jour:")
        self.messages_per_day_label.setFont(self.font)
        self.messages_per_day_input = QLineEdit(str(self.config.get('MESSAGES_PER_DAY', '10')))
        self.messages_per_day_input.setFont(self.font)
        self.main_layout.addWidget(self.messages_per_day_label)
        self.main_layout.addWidget(self.messages_per_day_input)

    def setup_start_button(self):
        """Configure le bouton pour démarrer le bot."""
        self.start_button = QPushButton("Start Bot")
        self.start_button.setFont(self.font)
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self.start_bot)
        self.main_layout.addWidget(self.start_button)

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

    def start_bot(self):
        """Démarre le bot après avoir effectué les validations."""
        logging.debug("Start Bot button clicked")

        if not self.validate_inputs():
            return

        self.save_configuration()
        self.run_bot()

    def validate_inputs(self):
        """Valide les entrées de l'utilisateur."""
        username = self.username_input.text()
        password = self.password_input.text()
        search_link = self.search_link_input.text()
        messages_per_day = self.messages_per_day_input.text()

        if not all([username, password, search_link, messages_per_day]):
            QMessageBox.warning(self, "Erreur de saisie", "Tous les champs doivent être remplis !")
            logging.error("Erreur de saisie : Tous les champs doivent être remplis !")
            return False

        # Valider le nombre de messages par jour
        try:
            self.messages_per_day_int = int(messages_per_day)
            if self.messages_per_day_int <= 0 or self.messages_per_day_int > 30:
                QMessageBox.warning(
                    self, "Erreur de saisie",
                    "Le nombre de messages par jour doit être entre 1 et 30 !"
                )
                logging.error(
                    "Erreur de saisie : Le nombre de messages par jour doit être entre 1 et 30 !"
                )
                return False
        except ValueError:
            QMessageBox.warning(
                self, "Erreur de saisie",
                "Le nombre de messages par jour doit être un nombre valide !"
            )
            logging.error("Erreur de saisie : Le nombre de messages par jour doit être un nombre valide !")
            return False

        return True

    def save_configuration(self):
        """Sauvegarde la configuration mise à jour."""
        logging.debug("Mise à jour de la configuration avec les nouvelles valeurs")
        self.config.update({
            'LINKEDIN_EMAIL': self.username_input.text(),
            'LINKEDIN_PASSWORD': self.password_input.text(),
            'LINKEDIN_SEARCH_LINK': self.search_link_input.text(),
            'MESSAGE_A': self.message_a_text,
            'MESSAGE_B': self.message_b_text,
            'MESSAGES_PER_DAY': self.messages_per_day_int
        })
        update_config(self.config)
        logging.debug("Configuration mise à jour avec succès")

    def run_bot(self):
        """Crée une instance du contrôleur et exécute le bot."""
        try:
            logging.debug("Création de l'instance MainController")
            self.controller = MainController(
                username=self.username_input.text(),
                password=self.password_input.text(),
                search_link=self.search_link_input.text(),
                message_a=self.message_a_text,
                message_b=self.message_b_text,
                messages_per_day=self.messages_per_day_int
            )
            logging.debug("Instance MainController créée")

            # Vérifier si la limite quotidienne de messages est atteinte
            limit_reached, messages_sent = self.controller.data_manager.has_reached_message_limit(self.messages_per_day_int)
            if limit_reached:
                QMessageBox.warning(
                    self, "Limite atteinte",
                    f"Le bot a déjà envoyé le nombre maximum de messages aujourd'hui ({messages_sent}/{self.messages_per_day_int})."
                )
                logging.info("Limite quotidienne de messages atteinte, le bot ne démarrera pas.")
                return

            logging.debug("Bot démarré avec succès")
            self.controller.run()
            logging.debug("Méthode run() de MainController appelée")
            QMessageBox.information(self, "Fin du bot", "Le bot a terminé son exécution.")

        except Exception as e:
            logging.error(f"Erreur lors de l'exécution du bot: {e}")
            QMessageBox.critical(self, "Erreur critique", f"Une erreur est survenue : {e}")

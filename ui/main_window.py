import logging
from requests import post

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QColor
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton,
    QMessageBox, QDialog, QTextEdit
)

from config.config import load_config, update_config
from constants.errors import LanguageError
from controllers.main_controller import MainController
from ui.styles import get_stylesheet
from utils.utils import get_resource_path


class MessageEditDialog(QDialog):
    def __init__(self, title, initial_text):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(400, 350)

        self.max_length = 300

        # Zone de texte pour éditer le message
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(initial_text)
        self.text_edit.textChanged.connect(self.update_character_count)

        # Label pour le compteur de caractères
        self.char_count_label = QLabel()
        self.char_count_label.setAlignment(Qt.AlignRight)
        self.char_count_label.setFont(QFont("Montserrat", 10))
        self.update_character_count()  # Initialiser le compteur

        # Bouton pour enregistrer le message
        self.save_button = QPushButton("Enregistrer")
        self.save_button.clicked.connect(self.accept)
        self.save_button.setFont(QFont("Montserrat", 10))

        # Mise en page de la boîte de dialogue
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.char_count_label)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def update_character_count(self):
        current_length = len(self.text_edit.toPlainText())
        if current_length > self.max_length:
            # Si la limite est dépassée, le compteur devient rouge
            self.char_count_label.setStyleSheet("color: red;")
        else:
            # Sinon, le compteur reste de couleur blanche
            self.char_count_label.setStyleSheet("color: white;")

        self.char_count_label.setText(f"{current_length}/{self.max_length} caractères")

    def accept(self):
        current_length = len(self.text_edit.toPlainText())
        if current_length > self.max_length:
            QMessageBox.warning(self, "Limite dépassée", f"Le message ne doit pas dépasser {self.max_length} caractères.")
        else:
            super().accept()

    def get_text(self):
        return self.text_edit.toPlainText()




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bot LinkedIn")

        # Définir l'icône de la fenêtre
        path_icon = get_resource_path("ui/resources/logo3d.png")
        self.setWindowIcon(QIcon(path_icon))
        self.resize(400, 600)

        # Charger la configuration
        self.config = load_config()

        # Charger la police Montserrat
        montserrat = QFont("Montserrat", 10)
        self.setStyleSheet(get_stylesheet())

        # Créer le layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Titre de l'application
        self.title_label = QLabel("Bot LinkedIn")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("title")
        self.title_label.setFont(montserrat)
        layout.addWidget(self.title_label)
        layout.addSpacing(30)

        # Champs de saisie pour l'email LinkedIn
        self.username_label = QLabel("Email LinkedIn:")
        self.username_label.setFont(montserrat)
        self.username_input = QLineEdit(self.config.get('LINKEDIN_EMAIL', ''))
        self.username_input.setFont(montserrat)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # Champs de saisie pour le mot de passe LinkedIn
        self.password_label = QLabel("Mot de passe LinkedIn:")
        self.password_label.setFont(montserrat)
        self.password_input = QLineEdit(self.config.get('LINKEDIN_PASSWORD', ''))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(montserrat)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Champs de saisie pour le lien de recherche
        self.search_link_label = QLabel("Lien de recherche:")
        self.search_link_label.setFont(montserrat)
        self.search_link_input = QLineEdit(self.config.get('LINKEDIN_SEARCH_LINK', ''))
        self.search_link_input.setFont(montserrat)
        layout.addWidget(self.search_link_label)
        layout.addWidget(self.search_link_input)

        # Initialiser les messages A et B
        self.message_a_text = self.config.get('MESSAGE_A', '')
        self.message_b_text = self.config.get('MESSAGE_B', '')

        # Section pour le Message Template A
        self.message_a_label = QLabel("Message Template A:")
        self.message_a_label.setFont(montserrat)
        layout.addWidget(self.message_a_label)

        self.message_a_button = QPushButton(self.get_message_preview(self.message_a_text))
        self.message_a_button.setFont(montserrat)
        self.message_a_button.setObjectName("messageButton")
        self.message_a_button.clicked.connect(self.edit_message_a)
        layout.addWidget(self.message_a_button)

        # Section pour le Message Template B
        self.message_b_label = QLabel("Message Template B:")
        self.message_b_label.setFont(montserrat)
        layout.addWidget(self.message_b_label)

        self.message_b_button = QPushButton(self.get_message_preview(self.message_b_text))
        self.message_b_button.setFont(montserrat)
        self.message_b_button.setObjectName("messageButton")
        self.message_b_button.clicked.connect(self.edit_message_b)
        layout.addWidget(self.message_b_button)

        # Champs de saisie pour le nombre de messages par jour
        self.messages_per_day_label = QLabel("Messages par jour:")
        self.messages_per_day_label.setFont(montserrat)
        self.messages_per_day_input = QLineEdit(str(self.config.get('MESSAGES_PER_DAY', '10')))
        self.messages_per_day_input.setFont(montserrat)
        layout.addWidget(self.messages_per_day_label)
        layout.addWidget(self.messages_per_day_input)

        # Champs de saisie pour la clé de licence
        self.license_key_label = QLabel("Clé de licence:")
        self.license_key_label.setFont(montserrat)
        self.license_key_input = QLineEdit(self.config.get('LICENSE_KEY', ''))
        self.license_key_input.setFont(montserrat)
        layout.addWidget(self.license_key_label)
        layout.addWidget(self.license_key_input)

        # Bouton pour démarrer le bot
        self.start_button = QPushButton("Start Bot")
        self.start_button.setFont(montserrat)
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self.start_bot)
        layout.addWidget(self.start_button)

        # Définir le widget central
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def get_message_preview(self, message):
        """Retourne un aperçu du message (50 premiers caractères)."""
        if message:
            preview = message[:50] + '...' if len(message) > 30 else message
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

    def verify_license(self, license_key):
        """Vérifie la validité de la clé de licence."""
        response = post(
            'https://licences-gen-bot.ew.r.appspot.com/verify_license',
            json={"license_key": license_key}
        )
        return response.json().get('valid', False)

    def start_bot(self):
        """Démarre le bot après avoir effectué toutes les vérifications."""
        logging.debug("Start Bot button clicked")

        username = self.username_input.text()
        password = self.password_input.text()
        search_link = self.search_link_input.text()
        message_a = self.message_a_text
        message_b = self.message_b_text
        messages_per_day = self.messages_per_day_input.text()
        license_key = self.license_key_input.text().replace(" ", "")

        if not all([username, password, search_link, message_a, message_b, messages_per_day, license_key]):
            QMessageBox.warning(self, "Erreur de saisie", "Tous les champs doivent être remplis !")
            logging.error("Erreur de saisie : Tous les champs doivent être remplis !")
            return

        # Vérifier que les messages ne dépassent pas 300 caractères
        if len(message_a) > 300:
            QMessageBox.warning(self, "Erreur de saisie", "Le Message A dépasse la limite de 300 caractères !")
            logging.error("Erreur de saisie : Le Message A dépasse la limite de 300 caractères !")
            return

        if len(message_b) > 300:
            QMessageBox.warning(self, "Erreur de saisie", "Le Message B dépasse la limite de 300 caractères !")
            logging.error("Erreur de saisie : Le Message B dépasse la limite de 300 caractères !")
            return

        # Vérifier que le nombre de messages par jour est valide
        try:
            messages_per_day_int = int(messages_per_day)
            if messages_per_day_int <= 0 or messages_per_day_int > 30:
                QMessageBox.warning(
                    self, "Erreur de saisie",
                    "Le nombre de messages par jour doit être supérieur ou égal à 1 et ne doit pas dépasser 30 !"
                )
                logging.error(
                    "Erreur de saisie : Le nombre de messages par jour doit être supérieur ou égal à 1 et ne doit pas dépasser 30 !"
                )
                return
        except ValueError:
            QMessageBox.warning(
                self, "Erreur de saisie",
                "Le nombre de messages par jour doit être un nombre valide !"
            )
            logging.error("Erreur de saisie : Le nombre de messages par jour doit être un nombre valide !")
            return

        # Vérifier la licence avant de continuer
        if not self.verify_license(license_key):
            QMessageBox.critical(
                self, "Erreur de licence",
                "Licence invalide. Veuillez vérifier votre clé de licence."
            )
            logging.error("Licence invalide. Fermeture...")
            return

        # Sauvegarder les nouvelles valeurs dans le fichier JSON
        try:
            logging.debug("Updating configuration with new values")
            self.config.update({
                'LINKEDIN_EMAIL': username,
                'LINKEDIN_PASSWORD': password,
                'LINKEDIN_SEARCH_LINK': search_link,
                'MESSAGE_A': message_a,
                'MESSAGE_B': message_b,
                'MESSAGES_PER_DAY': messages_per_day_int,
                'LICENSE_KEY': license_key
            })
            update_config(self.config)
            logging.debug("Configuration updated successfully")

            # Créer une instance du contrôleur principal
            logging.debug("Creating MainController instance")
            self.controller = MainController(
                username=username,
                password=password,
                search_link=search_link,
                message_a=message_a,
                message_b=message_b,
                messages_per_day=messages_per_day_int
            )
            logging.debug("MainController instance created")

            # Vérifier si la limite de messages quotidiens est atteinte
            limit_reached, messages_sent = self.controller.data_manager.has_reached_message_limit(messages_per_day_int)
            if limit_reached:
                QMessageBox.warning(
                    self, "Limite atteinte",
                    f"Le bot a déjà envoyé le nombre maximum de messages aujourd'hui ({messages_sent}/{messages_per_day_int})."
                )
                logging.info("Daily message limit reached, bot will not start.")
                return

            logging.debug("Bot started successfully")

            # Démarrer le bot
            self.controller.run()
            logging.debug("MainController run() called")
            QMessageBox.information(self, "Fin du bot", "Le bot a terminé son exécution.")

        except LanguageError as e:
            logging.error(f"Erreur de langue : {e}")
            QMessageBox.warning(self, "Erreur de langue", str(e))
        except Exception as e:
            logging.error(f"Error running the bot: {e}")
            QMessageBox.critical(self, "Erreur critique", f"Une erreur est survenue : {e}")

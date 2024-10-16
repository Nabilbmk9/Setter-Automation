# base_main_window.py

import logging
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton,
    QMessageBox, QDialog, QTextEdit
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

        # Définir l'icône de la fenêtre
        path_icon = get_resource_path("ui/resources/logo3d.png")
        self.setWindowIcon(QIcon(path_icon))
        self.resize(400, 600)

        # Charger la configuration
        self.config = load_config()

        # Charger la police Montserrat
        self.font = QFont("Montserrat", 10)
        self.setStyleSheet(get_stylesheet())

        # Créer le layout principal
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)

        # Définir le widget central
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Appeler la méthode pour configurer l'interface
        self.setup_ui()

    def setup_ui(self):
        """Configure l'interface utilisateur. Cette méthode sera surchargée dans les sous-classes."""
        pass

    def start_bot(self):
        """Démarre le bot après avoir effectué toutes les vérifications."""
        logging.debug("Start Bot button clicked")

        username = self.username_input.text()
        password = self.password_input.text()
        search_link = self.search_link_input.text()
        messages_per_day = self.messages_per_day_input.text()

        if not all([username, password, search_link, messages_per_day]):
            QMessageBox.warning(self, "Erreur de saisie", "Tous les champs doivent être remplis !")
            logging.error("Erreur de saisie : Tous les champs doivent être remplis !")
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

        # Sauvegarder les nouvelles valeurs dans le fichier JSON
        try:
            logging.debug("Mise à jour de la configuration avec les nouvelles valeurs")
            self.config.update({
                'LINKEDIN_EMAIL': username,
                'LINKEDIN_PASSWORD': password,
                'LINKEDIN_SEARCH_LINK': search_link,
                'MESSAGES_PER_DAY': messages_per_day_int
            })
            update_config(self.config)
            logging.debug("Configuration mise à jour avec succès")

            # Créer une instance du contrôleur principal
            logging.debug("Création de l'instance MainController")
            self.controller = MainController(
                username=username,
                password=password,
                search_link=search_link,
                messages_per_day=messages_per_day_int
            )
            logging.debug("Instance MainController créée")

            # Vérifier si la limite de messages quotidiens est atteinte
            limit_reached, messages_sent = self.controller.data_manager.has_reached_message_limit(messages_per_day_int)
            if limit_reached:
                QMessageBox.warning(
                    self, "Limite atteinte",
                    f"Le bot a déjà envoyé le nombre maximum de messages aujourd'hui ({messages_sent}/{messages_per_day_int})."
                )
                logging.info("Limite quotidienne de messages atteinte, le bot ne démarrera pas.")
                return

            logging.debug("Bot démarré avec succès")

            # Démarrer le bot
            self.controller.run()
            logging.debug("Méthode run() de MainController appelée")
            QMessageBox.information(self, "Fin du bot", "Le bot a terminé son exécution.")

        except Exception as e:
            logging.error(f"Erreur lors de l'exécution du bot: {e}")
            QMessageBox.critical(self, "Erreur critique", f"Une erreur est survenue : {e}")

# standard_main_window.py

from ui.base_main_window import BaseMainWindow
import logging
from PySide6.QtWidgets import QMessageBox
from controllers.main_controller import MainController

class StandardMainWindow(BaseMainWindow):
    def __init__(self):
        super().__init__()

    def setup_ui(self):
        """Configure l'UI pour les utilisateurs standard."""
        self.setup_title()
        self.setup_linkedin_credentials()
        self.setup_search_link()
        self.setup_message_templates()
        self.setup_messages_per_day()
        self.setup_start_button()

    def start_bot(self):
        """Démarre le bot pour les utilisateurs standard."""
        logging.debug("Start Bot button clicked (Standard)")

        # Valider les entrées
        if not self.validate_inputs():
            return

        # Sauvegarder la configuration
        self.save_configuration()

        # Exécuter le bot
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

        # Vérifier que les messages Template A et B ne sont pas vides
        if not self.message_a_text or not self.message_b_text:
            QMessageBox.warning(self, "Erreur de saisie", "Les messages Template A et B doivent être remplis !")
            logging.error("Erreur de saisie : Les messages Template A et B doivent être remplis !")
            return False

        return True

    def run_bot(self):
        """Crée une instance du contrôleur et exécute le bot."""
        try:
            logging.debug("Création de l'instance MainController (Standard)")
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

            logging.debug("Bot démarré avec succès (Standard)")
            self.controller.run()
            logging.debug("Méthode run() de MainController appelée")
            QMessageBox.information(self, "Fin du bot", "Le bot a terminé son exécution.")

        except Exception as e:
            logging.error(f"Erreur lors de l'exécution du bot: {e}")
            QMessageBox.critical(self, "Erreur critique", f"Une erreur est survenue : {e}")

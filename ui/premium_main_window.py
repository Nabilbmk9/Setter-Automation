# premium_main_window.py

from ui.base_main_window import BaseMainWindow
from ui.premium_features_mixin import PremiumFeaturesMixin
import logging
from PySide6.QtWidgets import QMessageBox

class PremiumMainWindow(PremiumFeaturesMixin, BaseMainWindow):
    def __init__(self):
        super().__init__()

    def setup_ui(self):
        """Configure l'UI pour les utilisateurs premium."""
        self.setup_title()
        self.setup_linkedin_credentials()
        self.setup_search_link()

        # Ajouter le choix du type de message juste après 'Lien de recherche'
        self.setup_message_type_selection()

        # Ajouter les messages Template A/B
        self.setup_message_templates()

        # Ajouter le champ 'Messages par jour'
        self.setup_messages_per_day()

        # Ajouter les éléments premium (clé API, prompt)
        self.setup_premium_ui()

        # Ajouter le bouton 'Start Bot' tout en bas
        self.setup_start_button()

    def start_bot(self):
        """Démarre le bot avec les fonctionnalités premium."""
        logging.debug("Start Bot button clicked (Premium)")

        # Valider les entrées premium (si ChatGPT est sélectionné)
        if self.chatgpt_message_radio.isChecked():
            if not self.validate_premium_inputs():
                return
            # Sauvegarder la configuration premium
            self.save_premium_configuration()
        else:
            # Sauvegarder la configuration pour le type normal
            self.save_premium_configuration()

        # Valider les entrées de base en tenant compte du type de message
        if not self.validate_inputs():
            return

        # Sauvegarder la configuration de base
        self.save_configuration()

        # Exécuter le bot avec les fonctionnalités premium
        self.run_premium_bot()

    def validate_inputs(self):
        """Valide les entrées de l'utilisateur en tenant compte du type de message."""
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

        # Validation supplémentaire en fonction du type de message
        if self.normal_message_radio.isChecked():
            # Vérifier que les messages Template A et B ne sont pas vides
            if not self.message_a_text or not self.message_b_text:
                QMessageBox.warning(self, "Erreur de saisie", "Les messages Template A et B doivent être remplis !")
                logging.error("Erreur de saisie : Les messages Template A et B doivent être remplis !")
                return False
        elif self.chatgpt_message_radio.isChecked():
            # Les validations pour ChatGPT sont déjà faites dans validate_premium_inputs
            pass
        else:
            QMessageBox.warning(self, "Erreur", "Type de message invalide.")
            logging.error("Erreur : Type de message invalide.")
            return False

        return True

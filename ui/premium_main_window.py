# premium_main_window.py
from PySide6.QtCore import Qt

from ui.base_main_window import BaseMainWindow
from ui.premium_features_mixin import PremiumFeaturesMixin
import logging
from PySide6.QtWidgets import QMessageBox, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy


class PremiumMainWindow(PremiumFeaturesMixin, BaseMainWindow):
    def __init__(self):
        super().__init__()

    def setup_ui(self):
        """Configure l'UI pour les utilisateurs premium."""
        # Créer le layout principal en vertical
        self.main_vertical_layout = QVBoxLayout()
        self.main_layout.addLayout(self.main_vertical_layout)

        # Créer le titre centré
        self.setup_title()
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_vertical_layout.addWidget(self.title_label)

        # Créer le layout principal en horizontal pour les colonnes
        self.columns_layout = QHBoxLayout()
        self.main_vertical_layout.addLayout(self.columns_layout)

        # Colonne 1 : Paramètres généraux
        self.general_column = QWidget()
        self.general_layout = QVBoxLayout()
        self.general_column.setLayout(self.general_layout)

        # Colonne 2 : Paramètres de messagerie
        self.messaging_column = QWidget()
        self.messaging_layout = QVBoxLayout()
        self.messaging_column.setLayout(self.messaging_layout)

        # Ajouter les colonnes au layout principal
        self.columns_layout.addWidget(self.general_column)
        self.columns_layout.addWidget(self.messaging_column)

        # Appeler les méthodes pour configurer les composants, en les ajoutant aux colonnes appropriées
        self.setup_general_column()
        self.setup_messaging_column()

        # Ajouter un espace vide pour pousser le bouton en bas
        self.main_vertical_layout.addStretch()

        # Si ce n'est pas un utilisateur Ultimate, ajouter le bouton 'Start Bot'
        if self.config.get('LICENSE_TYPE') != 'ultimate':
            # Ajouter le bouton "Start Bot" centré
            self.setup_start_button()
            self.start_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.start_button_layout = QHBoxLayout()
            self.start_button_layout.addStretch()
            self.start_button_layout.addWidget(self.start_button)
            self.start_button_layout.addStretch()

            # Ajouter le layout du bouton au layout principal vertical
            self.main_vertical_layout.addLayout(self.start_button_layout)

            # Ajuster la taille minimale de la fenêtre pour s'adapter aux colonnes
            self.setMinimumWidth(1200)

    def setup_general_column(self):
        """Configure les éléments de la colonne des paramètres généraux."""
        # Déplacer les composants dans le layout de la colonne générale
        self.setup_linkedin_credentials()
        self.general_layout.addWidget(self.username_label)
        self.general_layout.addWidget(self.username_input)
        self.general_layout.addWidget(self.password_label)
        self.general_layout.addWidget(self.password_input)

        self.setup_search_link()
        self.general_layout.addWidget(self.search_link_label)
        self.general_layout.addWidget(self.search_link_input)

        self.setup_messages_per_day()
        self.general_layout.addWidget(self.messages_per_day_label)
        self.general_layout.addWidget(self.messages_per_day_input)

        # Ajouter un espace vide pour pousser le contenu vers le haut
        self.general_layout.addStretch()

    def setup_messaging_column(self):
        """Configure les éléments de la colonne des paramètres de messagerie."""
        self.setup_message_type_selection()
        # Choix du type de message
        self.messaging_layout.addWidget(self.message_type_label)
        self.messaging_layout.addWidget(self.normal_message_radio)
        self.messaging_layout.addWidget(self.chatgpt_message_radio)

        # Messages Template A/B
        self.setup_message_templates()
        self.messaging_layout.addWidget(self.message_a_label)
        self.messaging_layout.addWidget(self.message_a_button)
        self.messaging_layout.addWidget(self.message_b_label)
        self.messaging_layout.addWidget(self.message_b_button)

        # Clé API OpenAI et prompt personnalisé
        self.setup_premium_ui()
        self.messaging_layout.addWidget(self.api_key_label)
        self.messaging_layout.addWidget(self.api_key_input)
        self.messaging_layout.addWidget(self.prompt_label)
        self.messaging_layout.addWidget(self.prompt_input)
        self.messaging_layout.addWidget(self.analyze_profiles_checkbox)
        self.messaging_layout.addWidget(self.relevance_prompt_label)
        self.messaging_layout.addWidget(self.relevance_prompt_input)

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

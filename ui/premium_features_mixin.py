# premium_features_mixin.py

from PySide6.QtWidgets import QLabel, QLineEdit, QTextEdit, QMessageBox, QRadioButton
from PySide6.QtGui import QFont
from config.config import update_config
import logging

from controllers.main_controller import MainController
from services.chatgpt_manager import ChatGPTManager


class PremiumFeaturesMixin:
    def setup_message_type_selection(self):
        """Configure les boutons radio pour le choix du type de message."""
        font = self.font

        # Choix du type de message
        self.message_type_label = QLabel("Type de message à envoyer:")
        self.message_type_label.setFont(font)
        self.main_layout.addWidget(self.message_type_label)

        # Boutons radio pour le choix
        self.normal_message_radio = QRadioButton("Messages normaux (Templates A/B)")
        self.normal_message_radio.setFont(font)
        self.normal_message_radio.setChecked(True)  # Par défaut
        self.main_layout.addWidget(self.normal_message_radio)

        self.chatgpt_message_radio = QRadioButton("Messages personnalisés avec ChatGPT")
        self.chatgpt_message_radio.setFont(font)
        self.main_layout.addWidget(self.chatgpt_message_radio)

        # Connecter les signaux pour afficher/masquer les champs correspondants
        self.normal_message_radio.toggled.connect(self.toggle_message_fields)
        self.chatgpt_message_radio.toggled.connect(self.toggle_message_fields)

    def setup_premium_ui(self):
        """Configure les éléments de l'interface spécifiques aux fonctionnalités premium."""
        font = self.font

        # Clé API pour OpenAI
        self.api_key_label = QLabel("Clé API OpenAI:")
        self.api_key_label.setFont(font)
        self.api_key_input = QLineEdit(self.config.get('OPENAI_API_KEY', ''))
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setFont(font)
        self.main_layout.addWidget(self.api_key_label)
        self.main_layout.addWidget(self.api_key_input)

        # Prompt personnalisé
        self.prompt_label = QLabel("Prompt personnalisé:")
        self.prompt_label.setFont(font)
        self.prompt_input = QTextEdit(self.config.get('CUSTOM_PROMPT', ''))
        self.prompt_input.setFont(font)
        self.main_layout.addWidget(self.prompt_label)
        self.main_layout.addWidget(self.prompt_input)

        # Au démarrage, afficher/masquer les champs en fonction du bouton sélectionné
        self.toggle_message_fields()

    def toggle_message_fields(self):
        """Afficher ou masquer les champs en fonction du choix de l'utilisateur."""
        if self.normal_message_radio.isChecked():
            # Afficher les messages Template A et B
            self.message_a_label.show()
            self.message_a_button.show()
            self.message_b_label.show()
            self.message_b_button.show()

            # Masquer les champs ChatGPT
            self.api_key_label.hide()
            self.api_key_input.hide()
            self.prompt_label.hide()
            self.prompt_input.hide()
        else:
            # Masquer les messages Template A et B
            self.message_a_label.hide()
            self.message_a_button.hide()
            self.message_b_label.hide()
            self.message_b_button.hide()

            # Afficher les champs ChatGPT
            self.api_key_label.show()
            self.api_key_input.show()
            self.prompt_label.show()
            self.prompt_input.show()

    def validate_premium_inputs(self):
        """Valide les entrées spécifiques aux fonctionnalités premium."""
        if self.chatgpt_message_radio.isChecked():
            api_key = self.api_key_input.text()
            custom_prompt = self.prompt_input.toPlainText()

            if not api_key or not custom_prompt:
                QMessageBox.warning(self, "Erreur de saisie", "Veuillez remplir tous les champs pour ChatGPT.")
                logging.error("Erreur de saisie : Les champs Clé API et Prompt doivent être remplis pour ChatGPT.")
                return False

            # Optionnellement, valider la clé API avec OpenAI ici si nécessaire
        return True

    def save_premium_configuration(self):
        """Sauvegarde la configuration spécifique aux fonctionnalités premium."""
        # Déterminer le type de message choisi
        if self.normal_message_radio.isChecked():
            message_type = 'normal'
        else:
            message_type = 'chatgpt'

        self.config.update({
            'MESSAGE_TYPE': message_type,
            'OPENAI_API_KEY': self.api_key_input.text(),
            'CUSTOM_PROMPT': self.prompt_input.toPlainText()
        })
        update_config(self.config)
        logging.debug("Configuration premium mise à jour avec succès")

    def run_premium_bot(self):
        """Exécute le bot avec les fonctionnalités premium."""
        if self.chatgpt_message_radio.isChecked():
            # Utiliser ChatGPT pour générer les messages
            openai_api_key = self.api_key_input.text()
            custom_prompt = self.prompt_input.toPlainText()

            # Créer une instance de ChatGPTManager
            self.chatgpt_manager = ChatGPTManager(api_key=openai_api_key, prompt=custom_prompt)

            # Créer le contrôleur avec le chatgpt_manager
            self.controller = MainController(
                username=self.username_input.text(),
                password=self.password_input.text(),
                search_link=self.search_link_input.text(),
                messages_per_day=self.messages_per_day_int,
                chatgpt_manager=self.chatgpt_manager
            )
        else:
            # Créer le contrôleur avec les messages Template A et B
            self.controller = MainController(
                username=self.username_input.text(),
                password=self.password_input.text(),
                search_link=self.search_link_input.text(),
                message_a=self.message_a_text,
                message_b=self.message_b_text,
                messages_per_day=self.messages_per_day_int
            )

        # Vérifier si la limite quotidienne de messages est atteinte
        limit_reached, messages_sent = self.controller.data_manager.has_reached_message_limit(self.messages_per_day_int)
        if limit_reached:
            QMessageBox.warning(
                self, "Limite atteinte",
                f"Le bot a déjà envoyé le nombre maximum de messages aujourd'hui ({messages_sent}/{self.messages_per_day_int})."
            )
            logging.info("Limite quotidienne de messages atteinte, le bot ne démarrera pas.")
            return

        # Démarrer le bot
        try:
            logging.debug("Bot démarré avec succès (Premium)")
            self.controller.run()
            logging.debug("Méthode run() de MainController appelée")
            QMessageBox.information(self, "Fin du bot", "Le bot a terminé son exécution.")
        except Exception as e:
            logging.error(f"Erreur lors de l'exécution du bot: {e}")
            QMessageBox.critical(self, "Erreur critique", f"Une erreur est survenue : {e}")

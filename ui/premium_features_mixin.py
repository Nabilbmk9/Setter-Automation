# premium_features_mixin.py

from PySide6.QtWidgets import QLabel, QLineEdit, QTextEdit, QMessageBox
from PySide6.QtGui import QFont
from config.config import update_config
import logging

class PremiumFeaturesMixin:
    def setup_premium_ui(self):
        """Configure les éléments de l'interface spécifiques aux fonctionnalités premium juste après 'Messages par jour'."""
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

    def validate_premium_inputs(self):
        """Valide les entrées spécifiques aux fonctionnalités premium."""
        api_key = self.api_key_input.text()
        custom_prompt = self.prompt_input.toPlainText()

        if not api_key or not custom_prompt:
            QMessageBox.warning(self, "Erreur de saisie", "Veuillez remplir tous les champs premium.")
            return False

        # Optionnellement, valider la clé API avec OpenAI ici si nécessaire
        return True

    def save_premium_configuration(self):
        """Sauvegarde la configuration spécifique aux fonctionnalités premium."""
        self.config.update({
            'OPENAI_API_KEY': self.api_key_input.text(),
            'CUSTOM_PROMPT': self.prompt_input.toPlainText()
        })
        update_config(self.config)
        logging.debug("Configuration premium mise à jour avec succès")

    def run_premium_bot(self):
        """Exécute le bot avec les fonctionnalités premium."""
        # Récupérer les configurations premium pour les utiliser dans le bot
        openai_api_key = self.api_key_input.text()
        custom_prompt = self.prompt_input.toPlainText()

        # Si nécessaire, générer des messages personnalisés avec OpenAI
        # Exemple de code pour générer un message :
        # generated_message = self.generate_message_with_chatgpt(openai_api_key, custom_prompt)

        # Ensuite, passer le message généré au contrôleur
        # self.controller.set_generated_message(generated_message)

        # Appeler la méthode run_bot originale
        super().run_bot()

    # Méthode pour intégrer OpenAI (exemple)
    # def generate_message_with_chatgpt(self, api_key, prompt):
    #     # Implémentez la logique pour interagir avec l'API OpenAI
    #     pass

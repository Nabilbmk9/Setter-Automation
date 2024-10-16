# premium_main_window.py

from base_main_window import BaseMainWindow
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox


class PremiumMainWindow(BaseMainWindow):
    def __init__(self):
        super().__init__()

    def setup_ui(self):
        """Configure l'interface utilisateur pour la licence premium."""
        # Appeler la configuration standard
        super().setup_ui()

        # Ajouter des fonctionnalités premium
        premium_label = QLabel("Fonctionnalités Premium")
        premium_label.setFont(self.font)
        premium_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(premium_label)

        # Champ pour la clé API OpenAI
        self.api_key_label = QLabel("Clé API OpenAI:")
        self.api_key_label.setFont(self.font)
        self.api_key_input = QLineEdit(self.config.get('OPENAI_API_KEY', ''))
        self.api_key_input.setFont(self.font)
        self.layout.addWidget(self.api_key_label)
        self.layout.addWidget(self.api_key_input)

        # Zone de texte pour le prompt personnalisé
        self.prompt_label = QLabel("Prompt personnalisé:")
        self.prompt_label.setFont(self.font)
        self.prompt_input = QTextEdit(self.config.get('CUSTOM_PROMPT', ''))
        self.prompt_input.setFont(self.font)
        self.layout.addWidget(self.prompt_label)
        self.layout.addWidget(self.prompt_input)

        # Bouton pour ajouter des fichiers (optionnel)
        # ...

        # Le reste de l'interface reste identique

    def start_bot(self):
        """Démarre le bot avec les fonctionnalités premium."""
        # Récupérer les informations supplémentaires
        api_key = self.api_key_input.text()
        custom_prompt = self.prompt_input.toPlainText()

        # Valider les champs spécifiques aux fonctionnalités premium
        if not api_key or not custom_prompt:
            QMessageBox.warning(self, "Erreur de saisie", "Veuillez remplir tous les champs premium.")
            return

        # Sauvegarder les informations premium
        self.config.update({
            'OPENAI_API_KEY': api_key,
            'CUSTOM_PROMPT': custom_prompt
        })
        update_config(self.config)

        # Appeler le start_bot de la classe de base pour les vérifications communes
        super().start_bot()

        # Vous pouvez ajouter du code spécifique pour démarrer le bot avec ChatGPT

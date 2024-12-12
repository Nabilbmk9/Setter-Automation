from PySide6.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QMessageBox


class OpenAISettingsFeature:
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager

        # Widget pour la configuration de la clé API OpenAI
        self.api_key_label = QLabel("Clé API OpenAI:")
        self.api_key_input = QLineEdit(self.config_manager.get('OPENAI_API_KEY', ''))
        self.api_key_input.setEchoMode(QLineEdit.Password)

        # Layout interne pour organiser les widgets
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.api_key_label)
        self.layout.addWidget(self.api_key_input)

    def setup(self):
        """Configuration initiale si nécessaire."""
        pass

    def validate(self):
        """Valide que la clé API est renseignée."""
        if not self.api_key_input.text().strip():
            QMessageBox.warning(self.parent, "Erreur de saisie", "Veuillez entrer une clé API OpenAI valide.")
            return False
        return True

    def save_configuration(self):
        """Sauvegarde la clé API dans le ConfigurationManager."""
        self.config_manager.update({
            'OPENAI_API_KEY': self.api_key_input.text().strip()
        })

    def reload_configuration(self):
        """Recharge la clé API depuis le ConfigurationManager."""
        api_key = self.config_manager.get('OPENAI_API_KEY', '')
        self.api_key_input.setText(api_key)

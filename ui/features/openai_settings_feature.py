from PySide6.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QMessageBox


class OpenAISettingsFeature:
    def __init__(self, parent, config_manager, message_type_feature):
        self.parent = parent
        self.config_manager = config_manager
        self.message_type_feature = message_type_feature

        # Widgets pour la configuration OpenAI
        self.api_key_label = QLabel("Clé API OpenAI:")
        self.api_key_input = QLineEdit(self.config_manager.get('OPENAI_API_KEY', ''))
        self.api_key_input.setEchoMode(QLineEdit.Password)

        self.assistant_id_label = QLabel("Assistant ID pour la prospection:")
        self.assistant_id_input = QLineEdit(self.config_manager.get('PROSPECTING_ASSISTANT_ID', ''))

        # Layout interne pour organiser les widgets
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.api_key_label)
        self.layout.addWidget(self.api_key_input)
        self.layout.addWidget(self.assistant_id_label)
        self.layout.addWidget(self.assistant_id_input)

    def setup(self):
        """Ne fait plus rien, car le layout interne est déjà configuré."""
        pass

    def validate(self):
        # Valider seulement si ChatGPT est sélectionné
        if self.message_type_feature.is_chatgpt_selected():
            if not self.api_key_input.text() or not self.assistant_id_input.text():
                QMessageBox.warning(self.parent, "Erreur de saisie", "Clé API et Assistant ID doivent être remplis pour ChatGPT.")
                return False
        return True

    def save_configuration(self):
        """Sauvegarde les paramètres OpenAI dans le ConfigurationManager."""
        self.config_manager.update({
            'OPENAI_API_KEY': self.api_key_input.text(),
            'PROSPECTING_ASSISTANT_ID': self.assistant_id_input.text()
        })

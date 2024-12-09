# ui/features/openai_settings_feature.py

from PySide6.QtWidgets import QLabel, QLineEdit, QMessageBox


class OpenAISettingsFeature:
    def __init__(self, parent, config_manager, message_type_feature):
        self.parent = parent
        self.config_manager = config_manager
        self.message_type_feature = message_type_feature

        self.api_key_label = QLabel("Clé API OpenAI:")
        self.api_key_input = QLineEdit(self.config_manager.get('OPENAI_API_KEY', ''))
        self.api_key_input.setEchoMode(QLineEdit.Password)

        self.assistant_id_label = QLabel("Assistant ID pour la prospection:")
        self.assistant_id_input = QLineEdit(self.config_manager.get('PROSPECTING_ASSISTANT_ID', ''))

    def setup(self):
        self.parent.main_layout.addWidget(self.api_key_label)
        self.parent.main_layout.addWidget(self.api_key_input)
        self.parent.main_layout.addWidget(self.assistant_id_label)
        self.parent.main_layout.addWidget(self.assistant_id_input)

    def validate(self):
        # Valider seulement si ChatGPT est sélectionné
        if self.message_type_feature.is_chatgpt_selected():
            if not self.api_key_input.text() or not self.assistant_id_input.text():
                QMessageBox.warning(self.parent, "Erreur de saisie", "Clé API et Assistant ID doivent être remplis pour ChatGPT.")
                return False
        return True

    def save_configuration(self):
        self.config_manager.update({
            'OPENAI_API_KEY': self.api_key_input.text(),
            'PROSPECTING_ASSISTANT_ID': self.assistant_id_input.text()
        })

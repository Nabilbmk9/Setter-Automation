# ui/features/auto_reply_feature.py

from PySide6.QtWidgets import QLabel, QLineEdit, QRadioButton, QButtonGroup, QVBoxLayout, QMessageBox

class AutoReplyFeature:
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager

        self.auto_reply_label = QLabel("Voulez-vous que l’IA réponde automatiquement aux messages privés ?")

        self.auto_reply_yes_radio = QRadioButton("Oui")
        self.auto_reply_no_radio = QRadioButton("Non")

        auto_reply_enabled = self.config_manager.get('AUTO_REPLY_ENABLED', False)
        if auto_reply_enabled:
            self.auto_reply_yes_radio.setChecked(True)
        else:
            self.auto_reply_no_radio.setChecked(True)

        self.auto_reply_assistant_id_label = QLabel("Assistant ID pour les réponses automatiques:")
        self.auto_reply_assistant_id_input = QLineEdit(self.config_manager.get('AUTO_REPLY_ASSISTANT_ID', ''))

    def setup(self):
        self.parent.main_layout.addWidget(self.auto_reply_label)
        self.parent.main_layout.addWidget(self.auto_reply_yes_radio)
        self.parent.main_layout.addWidget(self.auto_reply_no_radio)
        self.parent.main_layout.addWidget(self.auto_reply_assistant_id_label)
        self.parent.main_layout.addWidget(self.auto_reply_assistant_id_input)

        self.toggle_auto_reply_fields()
        self.auto_reply_yes_radio.toggled.connect(self.toggle_auto_reply_fields)

    def toggle_auto_reply_fields(self):
        visible = self.auto_reply_yes_radio.isChecked()
        self.auto_reply_assistant_id_label.setVisible(visible)
        self.auto_reply_assistant_id_input.setVisible(visible)

    def validate(self):
        if self.auto_reply_yes_radio.isChecked():
            if not self.auto_reply_assistant_id_input.text().strip():
                QMessageBox.warning(self.parent, "Erreur de saisie", "Veuillez entrer l'Assistant ID pour les réponses automatiques.")
                return False
        return True

    def save_configuration(self):
        auto_reply_enabled = self.auto_reply_yes_radio.isChecked()
        self.config_manager.update({
            'AUTO_REPLY_ENABLED': auto_reply_enabled,
            'AUTO_REPLY_ASSISTANT_ID': self.auto_reply_assistant_id_input.text().strip()
        })

from PySide6.QtWidgets import QLabel, QRadioButton, QButtonGroup

class AutoReplyFeature:
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager

        self.auto_reply_label = QLabel("Voulez-vous que l’IA réponde automatiquement aux messages privés ?")
        self.auto_reply_label.setWordWrap(True)

        self.auto_reply_yes_radio = QRadioButton("Oui")
        self.auto_reply_no_radio = QRadioButton("Non")

        self.auto_reply_group = QButtonGroup(self.parent)
        self.auto_reply_group.addButton(self.auto_reply_yes_radio)
        self.auto_reply_group.addButton(self.auto_reply_no_radio)

        auto_reply_enabled = self.config_manager.get('AUTO_REPLY_ENABLED', False)
        if auto_reply_enabled:
            self.auto_reply_yes_radio.setChecked(True)
        else:
            self.auto_reply_no_radio.setChecked(True)

    def setup(self):
        self.parent.main_layout.addWidget(self.auto_reply_label)
        self.parent.main_layout.addWidget(self.auto_reply_yes_radio)
        self.parent.main_layout.addWidget(self.auto_reply_no_radio)

    def is_auto_reply_enabled(self):
        return self.auto_reply_yes_radio.isChecked()

    def save_configuration(self):
        auto_reply_enabled = self.auto_reply_yes_radio.isChecked()
        self.config_manager.update({'AUTO_REPLY_ENABLED': auto_reply_enabled})

    def get_assistant_id(self):
        return self.config_manager.get('AUTO_REPLY_ASSISTANT_ID', '')

    def reload_configuration(self):
        auto_reply_enabled = self.config_manager.get('AUTO_REPLY_ENABLED', False)
        if auto_reply_enabled:
            self.auto_reply_yes_radio.setChecked(True)
        else:
            self.auto_reply_no_radio.setChecked(True)

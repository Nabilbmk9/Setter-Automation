# ui/features/message_type_feature.py

from PySide6.QtWidgets import QLabel, QRadioButton, QButtonGroup, QVBoxLayout, QWidget

class MessageTypeFeature:
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager

        self.message_type_label = QLabel("Type de message à envoyer:")
        self.normal_message_radio = QRadioButton("Messages normaux (Templates A/B)")
        self.chatgpt_message_radio = QRadioButton("Messages personnalisés avec ChatGPT")

        # Chargement de la config existante
        message_type = self.config_manager.get('MESSAGE_TYPE', 'normal')
        if message_type == 'normal':
            self.normal_message_radio.setChecked(True)
        else:
            self.chatgpt_message_radio.setChecked(True)

    def setup(self):
        self.parent.main_layout.addWidget(self.message_type_label)

        self.radio_button_group = QButtonGroup(self.parent)
        self.radio_button_group.addButton(self.normal_message_radio)
        self.radio_button_group.addButton(self.chatgpt_message_radio)

        self.parent.main_layout.addWidget(self.normal_message_radio)
        self.parent.main_layout.addWidget(self.chatgpt_message_radio)

    def validate(self):
        # Ici, au moins un des boutons radio doit être coché, ce qui est déjà assuré.
        return True

    def save_configuration(self):
        message_type = 'custom' if self.chatgpt_message_radio.isChecked() else 'normal'
        self.config_manager.update({'MESSAGE_TYPE': message_type})

    def is_chatgpt_selected(self):
        return self.chatgpt_message_radio.isChecked()

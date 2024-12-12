# message_templates_feature.py

from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout
from ui.message_edit_dialog import MessageEditDialog

class MessageTemplatesFeature:
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager

        self.message_a_text = self.config_manager.get('MESSAGE_A', '')
        self.message_b_text = self.config_manager.get('MESSAGE_B', '')

        self.message_a_label = QLabel("Message Template A:")
        self.message_a_button = QPushButton(self.get_message_preview(self.message_a_text))
        self.message_a_button.clicked.connect(self.edit_message_a)

        self.message_b_label = QLabel("Message Template B:")
        self.message_b_button = QPushButton(self.get_message_preview(self.message_b_text))
        self.message_b_button.clicked.connect(self.edit_message_b)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.message_a_label)
        self.layout.addWidget(self.message_a_button)
        self.layout.addWidget(self.message_b_label)
        self.layout.addWidget(self.message_b_button)

    def get_message_preview(self, message):
        if message:
            return message[:50] + '...' if len(message) > 50 else message
        return "Message vide, cliquez pour remplir"

    def edit_message_a(self):
        dialog = MessageEditDialog("Éditer Message Template A", self.message_a_text)
        if dialog.exec():
            self.message_a_text = dialog.get_text()
            self.update_buttons_text()

    def edit_message_b(self):
        dialog = MessageEditDialog("Éditer Message Template B", self.message_b_text)
        if dialog.exec():
            self.message_b_text = dialog.get_text()
            self.update_buttons_text()

    def validate(self):
        # Ne pas afficher de QMessageBox ici, juste retourner False si invalide
        if not self.message_a_text or not self.message_b_text:
            return False
        return True

    def save_configuration(self):
        self.config_manager.update({
            'MESSAGE_A': self.message_a_text,
            'MESSAGE_B': self.message_b_text
        })

    def reload_configuration(self):
        # Recharge les valeurs depuis le config_manager
        self.message_a_text = self.config_manager.get('MESSAGE_A', '')
        self.message_b_text = self.config_manager.get('MESSAGE_B', '')
        self.update_buttons_text()

    def update_buttons_text(self):
        self.message_a_button.setText(self.get_message_preview(self.message_a_text))
        self.message_b_button.setText(self.get_message_preview(self.message_b_text))

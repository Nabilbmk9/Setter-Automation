from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from ui.message_edit_dialog import MessageEditDialog


class MessageConfigPage(QWidget):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)  # Le parent est transmis correctement ici
        self.config_manager = config_manager

        self.message_a_text = self.config_manager.get('MESSAGE_A', '')
        self.message_b_text = self.config_manager.get('MESSAGE_B', '')

        self.message_a_label = QLabel("Message Template A:")
        self.message_a_button = QPushButton(self.get_message_preview(self.message_a_text))
        self.message_a_button.setObjectName("messageButton")
        self.message_a_button.clicked.connect(self.edit_message_a)

        self.message_b_label = QLabel("Message Template B:")
        self.message_b_button = QPushButton(self.get_message_preview(self.message_b_text))
        self.message_b_button.setObjectName("messageButton")
        self.message_b_button.clicked.connect(self.edit_message_b)

        self.btn_enregistrer = QPushButton("Enregistrer")
        self.btn_annuler = QPushButton("Annuler")

        layout = QVBoxLayout()
        layout.addWidget(self.message_a_label)
        layout.addWidget(self.message_a_button)
        layout.addWidget(self.message_b_label)
        layout.addWidget(self.message_b_button)
        layout.addWidget(self.btn_enregistrer)
        layout.addWidget(self.btn_annuler)

        self.setLayout(layout)

    def get_message_preview(self, message):
        if message:
            return message[:50] + '...' if len(message) > 50 else message
        return "Message vide, cliquez pour remplir"

    def edit_message_a(self):
        dialog = MessageEditDialog("Éditer Message Template A", self.message_a_text)
        if dialog.exec():
            self.message_a_text = dialog.get_text()
            self.message_a_button.setText(self.get_message_preview(self.message_a_text))

    def edit_message_b(self):
        dialog = MessageEditDialog("Éditer Message Template B", self.message_b_text)
        if dialog.exec():
            self.message_b_text = dialog.get_text()
            self.message_b_button.setText(self.get_message_preview(self.message_b_text))

    def save_configuration(self):
        """Sauvegarde les messages dans le ConfigurationManager."""
        self.config_manager.update({
            'MESSAGE_A': self.message_a_text,
            'MESSAGE_B': self.message_b_text
        })

    def validate(self):
        """Valide les messages avant la sauvegarde."""
        if not self.message_a_text or not self.message_b_text:
            QMessageBox.warning(
                self, "Erreur de saisie",
                "Les messages Template A et B doivent être remplis !"
            )
            return False
        return True

# ui/features/linkedin_credentials_feature.py

from PySide6.QtWidgets import QLabel, QLineEdit, QMessageBox


class LinkedInCredentialsFeature:
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager

        self.username_label = QLabel("Email LinkedIn:")
        self.username_input = QLineEdit(self.config_manager.get('LINKEDIN_EMAIL', ''))

        self.password_label = QLabel("Mot de passe LinkedIn:")
        self.password_input = QLineEdit(self.config_manager.get('LINKEDIN_PASSWORD', ''))
        self.password_input.setEchoMode(QLineEdit.Password)

    def setup(self):
        self.parent.main_layout.addWidget(self.username_label)
        self.parent.main_layout.addWidget(self.username_input)
        self.parent.main_layout.addWidget(self.password_label)
        self.parent.main_layout.addWidget(self.password_input)

    def validate(self):
        if not self.username_input.text() or not self.password_input.text():
            QMessageBox.warning(self.parent, "Erreur de saisie", "Les champs LinkedIn doivent être remplis !")
            return False
        return True

    def save_configuration(self):
        self.config_manager.update({
            'LINKEDIN_EMAIL': self.username_input.text(),
            'LINKEDIN_PASSWORD': self.password_input.text(),
        })

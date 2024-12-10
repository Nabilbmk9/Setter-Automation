from PySide6.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QMessageBox


class ProspectingAssistantFeature:
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager

        # Widgets pour la configuration de l'Assistant ID
        self.assistant_id_label = QLabel("Assistant ID pour la prospection:")
        self.assistant_id_input = QLineEdit(self.config_manager.get('PROSPECTING_ASSISTANT_ID', ''))

        # Layout interne
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.assistant_id_label)
        self.layout.addWidget(self.assistant_id_input)

    def setup(self):
        """Configuration initiale si nécessaire."""
        pass

    def validate(self):
        """Valide que l'Assistant ID est renseigné."""
        if not self.assistant_id_input.text().strip():
            QMessageBox.warning(self.parent, "Erreur de saisie", "Veuillez entrer un Assistant ID valide pour la prospection.")
            return False
        return True

    def save_configuration(self):
        """Sauvegarde l'Assistant ID dans la configuration."""
        self.config_manager.update({
            'PROSPECTING_ASSISTANT_ID': self.assistant_id_input.text().strip()
        })

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton


class IAConfigPage(QWidget):
    def __init__(self, openai_settings_feature, parent=None):
        super().__init__(parent)
        self.openai_settings_feature = openai_settings_feature

        # Boutons Enregistrer et Annuler
        self.btn_enregistrer = QPushButton("Enregistrer")
        self.btn_annuler = QPushButton("Annuler")

        # Layout principal
        self.layout = QVBoxLayout()

        # Intégrer le layout d'OpenAISettingsFeature
        self.layout.addLayout(self.openai_settings_feature.layout)

        # Ajouter les boutons au layout
        self.layout.addWidget(self.btn_enregistrer)
        self.layout.addWidget(self.btn_annuler)

        self.setLayout(self.layout)

        # Connexions
        self.btn_enregistrer.clicked.connect(self.save_configuration)

    def validate(self):
        """Valide les paramètres OpenAI via OpenAISettingsFeature."""
        return self.openai_settings_feature.validate()

    def save_configuration(self):
        """Sauvegarde les paramètres OpenAI via OpenAISettingsFeature."""
        if self.validate():
            self.openai_settings_feature.save_configuration()

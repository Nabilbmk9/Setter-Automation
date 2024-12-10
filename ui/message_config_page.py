from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from ui.features.message_templates_feature import MessageTemplatesFeature


class MessageConfigPage(QWidget):
    def __init__(self, message_templates_feature, parent=None):
        super().__init__(parent)
        self.message_templates_feature = message_templates_feature

        # Boutons Enregistrer et Annuler
        self.btn_enregistrer = QPushButton("Enregistrer")
        self.btn_annuler = QPushButton("Annuler")

        # Layout principal
        self.layout = QVBoxLayout()

        # Intégrer le layout de MessageTemplatesFeature
        self.layout.addLayout(self.message_templates_feature.layout)

        # Ajouter les boutons au layout
        self.layout.addWidget(self.btn_enregistrer)
        self.layout.addWidget(self.btn_annuler)

        self.setLayout(self.layout)

        # Connexions
        self.btn_enregistrer.clicked.connect(self.save_configuration)

    def validate(self):
        """Valide les messages via MessageTemplatesFeature."""
        return self.message_templates_feature.validate()

    def save_configuration(self):
        """Sauvegarde les messages via MessageTemplatesFeature."""
        if self.validate():
            self.message_templates_feature.save_configuration()

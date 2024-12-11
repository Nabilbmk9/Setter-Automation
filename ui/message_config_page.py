from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from ui.features.message_templates_feature import MessageTemplatesFeature
from ui.features.title_feature import TitleFeature


class MessageConfigPage(QWidget):
    def __init__(self, message_templates_feature, parent=None, config_manager=None):
        super().__init__(parent)
        self.message_templates_feature = message_templates_feature

        # Initialiser le layout principal
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(15, 5, 15, 15) # Gauche, haut, droite, bas

        # Intégrer le titre
        self.title_feature = TitleFeature(self, config_manager)
        self.title_feature.add_to_layout(self.layout)

        # Boutons Enregistrer et Annuler
        self.btn_enregistrer = QPushButton("Enregistrer")
        self.btn_annuler = QPushButton("Annuler")

        self.btn_enregistrer.setObjectName("btnEnregistrer")
        self.btn_annuler.setObjectName("btnAnnuler")

        # Intégrer le layout de MessageTemplatesFeature
        self.layout.addLayout(self.message_templates_feature.layout)

        # Ajouter les boutons au layout
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.btn_enregistrer)
        self.buttons_layout.addWidget(self.btn_annuler)
        self.layout.addLayout(self.buttons_layout)

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

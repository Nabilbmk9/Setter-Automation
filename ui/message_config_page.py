from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
from ui.features.message_templates_feature import MessageTemplatesFeature
from ui.features.title_feature import TitleFeature


class MessageConfigPage(QWidget):
    def __init__(self, message_templates_feature, parent=None, config_manager=None):
        super().__init__(parent)
        self.message_templates_feature = message_templates_feature

        # Initialiser le layout principal
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(15, 5, 15, 15)  # Gauche, haut, droite, bas

        # Intégrer le titre
        self.title_feature = TitleFeature(self, config_manager)
        self.title_feature.add_to_layout(self.layout)

        # Sous-titre
        subtitle_label = QLabel("Configuration Message standard")
        subtitle_label.setObjectName("subtitle")
        self.layout.addWidget(subtitle_label)

        # Texte explicatif
        variables_label = QLabel(
            "Vous pouvez utiliser des variables pour personnaliser votre message.<br>"
            "Variables disponibles : <span style='color: #ff4500;'>{first_name}</span> et "
            "<span style='color: #ff4500;'>{last_name}</span>.<br>"
            "<br>"
            "⚠ Il faut que la variable soit exactement écrite de la même façon."
        )
        variables_label.setObjectName("subtitleText")
        variables_label.setWordWrap(True)  # Permet de couper le texte automatiquement si la largeur est limitée
        self.layout.addWidget(variables_label)

        # Intégrer le layout de MessageTemplatesFeature
        self.layout.addLayout(self.message_templates_feature.layout)

        self.layout.addStretch()

        # Boutons Enregistrer et Annuler
        self.btn_enregistrer = QPushButton("Enregistrer")
        self.btn_annuler = QPushButton("Annuler")

        self.btn_enregistrer.setObjectName("btnEnregistrer")
        self.btn_annuler.setObjectName("btnAnnuler")

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

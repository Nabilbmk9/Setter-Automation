# message_config_page.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QMessageBox
from ui.features.title_feature import TitleFeature

class MessageConfigPage(QWidget):
    def __init__(self, message_templates_feature, parent=None, config_manager=None):
        super().__init__(parent)
        self.message_templates_feature = message_templates_feature
        self.config_manager = config_manager

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(15, 5, 15, 15)

        self.title_feature = TitleFeature(self, config_manager)
        self.title_feature.add_to_layout(self.layout)

        subtitle_label = QLabel("Configuration Message standard")
        subtitle_label.setObjectName("subtitle")
        self.layout.addWidget(subtitle_label)

        variables_label = QLabel(
            "Vous pouvez utiliser des variables pour personnaliser votre message.<br>"
            "Variables disponibles : <span style='color: #ff4500;'>{first_name}</span> et "
            "<span style='color: #ff4500;'>{last_name}</span>.<br><br>"
            "⚠ Il faut que la variable soit exactement écrite de la même façon."
        )
        variables_label.setObjectName("subtitleText")
        variables_label.setWordWrap(True)
        self.layout.addWidget(variables_label)

        self.layout.addLayout(self.message_templates_feature.layout)

        self.layout.addStretch()

        self.btn_enregistrer = QPushButton("Enregistrer")
        self.btn_annuler = QPushButton("Annuler")

        self.btn_enregistrer.setObjectName("btnEnregistrer")
        self.btn_annuler.setObjectName("btnAnnuler")

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.btn_enregistrer)
        self.buttons_layout.addWidget(self.btn_annuler)
        self.layout.addLayout(self.buttons_layout)

        self.setLayout(self.layout)

    def validate(self):
        # Ne pas afficher de message ici
        return self.message_templates_feature.validate()

    def save_configuration(self):
        if not self.validate():
            QMessageBox.warning(self, "Erreur de saisie", "Les messages Template A et B doivent être remplis !")
            return False
        self.message_templates_feature.save_configuration()
        self.config_manager.save()
        return True

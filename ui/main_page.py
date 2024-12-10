from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QCheckBox, QRadioButton,
    QButtonGroup, QPushButton, QSpinBox, QLabel
)
from PySide6.QtCore import Slot

class MainPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Champs principaux
        self.linkedin_email = QLineEdit()
        self.linkedin_password = QLineEdit()
        self.linkedin_password.setEchoMode(QLineEdit.Password)
        self.search_link = QLineEdit()
        self.messages_per_day = QSpinBox()
        self.messages_per_day.setRange(0, 10000)

        # Type de message
        self.radio_normal = QRadioButton("Messages normaux")
        self.radio_custom = QRadioButton("Messages personnalisés (IA)")
        self.radio_group = QButtonGroup()
        self.radio_group.addButton(self.radio_normal)
        self.radio_group.addButton(self.radio_custom)
        self.radio_normal.setChecked(True)

        # Options IA
        self.check_analyse_profil = QCheckBox("Analyser les profils avec l'IA ?")
        self.check_auto_reply = QCheckBox("Réponses automatiques avec IA ?")

        # Boutons
        self.btn_configurer_messages = QPushButton("Configurer les messages")
        self.btn_configurer_ia = QPushButton("Configurer l'IA")

        # Mise en page
        form_layout = QFormLayout()
        form_layout.addRow("LinkedIn Email :", self.linkedin_email)
        form_layout.addRow("LinkedIn Password :", self.linkedin_password)
        form_layout.addRow("Lien de recherche :", self.search_link)
        form_layout.addRow("Messages par jour :", self.messages_per_day)

        type_layout = QVBoxLayout()
        type_layout.addWidget(QLabel("Type de message :"))
        type_layout.addWidget(self.radio_normal)
        type_layout.addWidget(self.radio_custom)

        ia_layout = QVBoxLayout()
        ia_layout.addWidget(self.check_analyse_profil)
        ia_layout.addWidget(self.check_auto_reply)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(type_layout)
        main_layout.addLayout(ia_layout)
        main_layout.addWidget(self.btn_configurer_messages)
        main_layout.addWidget(self.btn_configurer_ia)
        main_layout.addStretch()

        self.setLayout(main_layout)

        # Signaux
        self.radio_normal.toggled.connect(self.update_buttons)
        self.radio_custom.toggled.connect(self.update_buttons)
        self.check_analyse_profil.stateChanged.connect(self.update_buttons)
        self.check_auto_reply.stateChanged.connect(self.update_buttons)

        # Mise à jour initiale
        self.update_buttons()

    @Slot()
    def update_buttons(self):
        is_normal = self.radio_normal.isChecked()
        is_custom = self.radio_custom.isChecked()
        analyse_ia = self.check_analyse_profil.isChecked()
        auto_ia = self.check_auto_reply.isChecked()

        self.btn_configurer_messages.setVisible(is_normal)
        self.btn_configurer_ia.setVisible(is_custom or analyse_ia or auto_ia)

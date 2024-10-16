# ui/license_window.py

import logging
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from utils.license_utils import verify_license
from config.config import update_config
from ui.styles import get_stylesheet


class LicenseWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Activation du logiciel")
        self.setStyleSheet(get_stylesheet())
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.info_label = QLabel("Veuillez entrer votre clé de licence pour activer le logiciel.")
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)

        self.license_key_input = QLineEdit()
        self.license_key_input.setPlaceholderText("Clé de licence")
        layout.addWidget(self.license_key_input)

        self.activate_button = QPushButton("Activer")
        self.activate_button.clicked.connect(self.activate_license)
        layout.addWidget(self.activate_button)

        self.setLayout(layout)

    def activate_license(self):
        license_key = self.license_key_input.text().replace(" ", "")
        if not license_key:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer une clé de licence.")
            return

        valid, license_type = verify_license(license_key)
        if valid is None:
            QMessageBox.critical(self, "Erreur",
                                 "Impossible de vérifier la licence. Veuillez vérifier votre connexion internet.")
        elif valid:
            # Enregistrer la licence dans la configuration
            update_config({'LICENSE_KEY': license_key})
            QMessageBox.information(self, "Succès", "Licence activée avec succès.")
            self.accept()
        else:
            QMessageBox.critical(self, "Erreur", "Licence invalide ou expirée. Veuillez vérifier votre clé de licence.")

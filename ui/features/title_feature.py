# ui/features/title_feature.py

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

class TitleFeature:
    def __init__(self, parent, config_manager=None):
        """
        parent : Fenêtre parente où le titre sera affiché.
        config_manager : Optionnel. Permet de charger une version dynamique si nécessaire.
        """
        self.parent = parent
        self.title_label = QLabel("Bot LinkedIn")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("title")

        self.version_label = QLabel(f"Version {config_manager.get('VERSION', '1.0')}" if config_manager else "Version 1.0")
        self.version_label.setAlignment(Qt.AlignCenter)
        self.version_label.setObjectName("version")

    def setup(self):
        """
        Ajoute le titre et le label de version au layout principal.
        """
        self.parent.main_layout.addWidget(self.title_label)
        self.parent.main_layout.addWidget(self.version_label)
        self.parent.main_layout.addSpacing(30)

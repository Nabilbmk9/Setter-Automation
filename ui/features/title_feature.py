# ui/features/title_feature.py

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


class TitleFeature:
    def __init__(self, parent, config_manager=None):
        self.parent = parent
        self.title_label = QLabel("Bot LinkedIn")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("title")

        self.version_label = QLabel(f"Version {config_manager.get('VERSION', '1.0')}" if config_manager else "Version 1.0")
        self.version_label.setAlignment(Qt.AlignCenter)
        self.version_label.setObjectName("version")

    def setup(self):
        """Ajoute le titre et le label de version au layout principal."""
        self.parent.main_layout.addWidget(self.title_label)
        self.parent.main_layout.addWidget(self.version_label)
        self.parent.main_layout.addSpacing(20)

    def add_to_layout(self, layout):
        """Ajoute le titre et la version à un layout spécifique."""

        layout.addWidget(self.title_label)
        layout.addWidget(self.version_label)
        layout.addSpacing(20)

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QRadioButton, QButtonGroup, QToolTip


class TestModeFeature:
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager

        # Question pour activer le mode test
        self.question_label = QLabel("Voulez-vous activer le mode test ?    ℹ️")
        self.question_label.setCursor(Qt.PointingHandCursor)  # Ajoute un curseur interactif

        # Connecter l'événement de la souris pour afficher le tooltip
        self.question_label.mousePressEvent = self.show_tooltip

        # Options Oui/Non
        self.yes_radio_button = QRadioButton("Oui")
        self.no_radio_button = QRadioButton("Non")

        # Groupe de boutons pour gérer les choix
        self.radio_group = QButtonGroup()
        self.radio_group.addButton(self.yes_radio_button)
        self.radio_group.addButton(self.no_radio_button)

        # Charger l'état initial depuis la configuration
        test_mode_enabled = self.config_manager.get('TEST_MODE_ENABLED', False)
        if test_mode_enabled:
            self.yes_radio_button.setChecked(True)
        else:
            self.no_radio_button.setChecked(True)

        # Layout interne pour organiser la question et les boutons
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.question_label)
        self.layout.addWidget(self.yes_radio_button)
        self.layout.addWidget(self.no_radio_button)

    def show_tooltip(self, event):
        """Affiche le tooltip immédiatement avec une durée personnalisée."""
        QToolTip.showText(
            event.globalPos(),  # Position globale de la souris
            "Le mode test vous permet de vérifier le message généré par ChatGPT avant l'envoi.\n"
            "Si le message ne vous convient pas, ajustez le prompt et cliquez sur 'Réessayer'.",
            self.question_label,  # Widget cible
            msecShowTime=5000  # Durée d'affichage en millisecondes (5 secondes ici)
        )

    def setup(self):
        """Ajoute la question et les boutons au layout principal de la fenêtre parente."""
        self.parent.main_layout.addLayout(self.layout)

    def validate(self):
        """Toujours valide, aucun traitement spécifique ici."""
        return True

    def save_configuration(self):
        """Sauvegarde l'état sélectionné dans la configuration."""
        self.config_manager.update({
            'TEST_MODE_ENABLED': self.yes_radio_button.isChecked()
        })

    def is_test_mode_enabled(self):
        """Renvoie True si le mode test est activé."""
        return self.yes_radio_button.isChecked()

    def reload_configuration(self):
        test_mode_enabled = self.config_manager.get('TEST_MODE_ENABLED', False)
        if test_mode_enabled:
            self.yes_radio_button.setChecked(True)
        else:
            self.no_radio_button.setChecked(True)
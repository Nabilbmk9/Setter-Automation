# ultimate_main_window.py

from ui.premium_main_window import PremiumMainWindow
from PySide6.QtWidgets import QLabel, QCheckBox, QTextEdit, QMessageBox
import logging
from config.config import update_config

class UltimateMainWindow(PremiumMainWindow):
    def __init__(self):
        super().__init__()

    def setup_ui(self):
        """Configure l'UI pour les utilisateurs Ultimate."""
        # Appeler la méthode setup_ui de la classe parent
        super().setup_ui()

        # Ajouter les composants spécifiques au plan Ultimate
        self.setup_ultimate_features()

        # Ajouter le bouton "Start Bot" tout en bas
        self.setup_start_button()

    def setup_ultimate_features(self):
        """Ajoute les fonctionnalités spécifiques au plan Ultimate."""
        font = self.font

        # Case à cocher pour activer la réponse automatique
        self.auto_reply_checkbox = QCheckBox("Activer la réponse automatique")
        self.auto_reply_checkbox.setFont(font)
        self.auto_reply_checkbox.stateChanged.connect(self.toggle_auto_reply_fields)
        self.main_layout.addWidget(self.auto_reply_checkbox)

        # Champ pour le prompt de réponse automatique
        self.auto_reply_prompt_label = QLabel("Prompt pour les réponses automatiques:")
        self.auto_reply_prompt_label.setFont(font)
        self.auto_reply_prompt_input = QTextEdit(self.config.get('AUTO_REPLY_PROMPT', ''))
        self.auto_reply_prompt_input.setFont(font)
        self.main_layout.addWidget(self.auto_reply_prompt_label)
        self.main_layout.addWidget(self.auto_reply_prompt_input)

        # Masquer les champs de réponse automatique par défaut
        self.auto_reply_prompt_label.hide()
        self.auto_reply_prompt_input.hide()

        # Charger l'état de la case à cocher depuis la configuration
        auto_reply_enabled = self.config.get('AUTO_REPLY_ENABLED', False)
        self.auto_reply_checkbox.setChecked(auto_reply_enabled)

    def toggle_auto_reply_fields(self):
        """Afficher ou masquer les champs de réponse automatique."""
        if self.auto_reply_checkbox.isChecked():
            self.auto_reply_prompt_label.show()
            self.auto_reply_prompt_input.show()
        else:
            self.auto_reply_prompt_label.hide()
            self.auto_reply_prompt_input.hide()

    def validate_inputs(self):
        """Valide les entrées de l'utilisateur en tenant compte du plan Ultimate."""
        # Appeler la validation de la classe parent
        if not super().validate_inputs():
            return False

        # Valider les entrées spécifiques au plan Ultimate
        if self.auto_reply_checkbox.isChecked():
            auto_reply_prompt = self.auto_reply_prompt_input.toPlainText()
            if not auto_reply_prompt:
                QMessageBox.warning(self, "Erreur de saisie", "Veuillez remplir le prompt pour les réponses automatiques.")
                logging.error("Erreur de saisie : Le prompt pour les réponses automatiques doit être rempli.")
                return False

        return True

    def save_configuration(self):
        """Sauvegarde la configuration mise à jour, y compris les paramètres Ultimate."""
        # Appeler la méthode de sauvegarde de la classe parent
        super().save_configuration()

        # Enregistrer les paramètres Ultimate
        auto_reply_enabled = self.auto_reply_checkbox.isChecked()
        auto_reply_prompt = self.auto_reply_prompt_input.toPlainText()

        self.config.update({
            'AUTO_REPLY_ENABLED': auto_reply_enabled,
            'AUTO_REPLY_PROMPT': auto_reply_prompt,
        })
        update_config(self.config)
        logging.debug("Configuration Ultimate mise à jour avec succès")

    def run_bot(self):
        """Exécute le bot avec les fonctionnalités Ultimate."""
        # Vous pouvez surcharger cette méthode pour inclure les fonctionnalités Ultimate
        # ou appeler la méthode de la classe parent si elle convient
        self.run_ultimate_bot()

    def run_ultimate_bot(self):
        """Exécute le bot avec les fonctionnalités spécifiques au plan Ultimate."""
        # Appeler la méthode de la classe parent pour initialiser le bot
        super().run_premium_bot()

        # Ici, vous pouvez ajouter du code pour démarrer la réponse automatique
        # Nous implémenterons cela dans les étapes suivantes

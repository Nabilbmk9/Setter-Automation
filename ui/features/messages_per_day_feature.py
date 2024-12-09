# ui/features/messages_per_day_feature.py

from PySide6.QtWidgets import QLabel, QLineEdit, QMessageBox
import logging


class MessagesPerDayFeature:
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager

        self.messages_per_day_label = QLabel("Messages par jour:")
        self.messages_per_day_input = QLineEdit(str(self.config_manager.get('MESSAGES_PER_DAY', '10')))
        self._messages_per_day_int = None  # Stockera la valeur validée

    def setup(self):
        self.parent.main_layout.addWidget(self.messages_per_day_label)
        self.parent.main_layout.addWidget(self.messages_per_day_input)

    def validate(self):
        messages_per_day_str = self.messages_per_day_input.text().strip()
        if not messages_per_day_str:
            QMessageBox.warning(self.parent, "Erreur de saisie", "Le nombre de messages par jour ne peut pas être vide !")
            logging.error("Erreur de saisie : Le nombre de messages par jour est vide.")
            return False

        try:
            value = int(messages_per_day_str)
            if value <= 0 or value > 30:
                QMessageBox.warning(
                    self.parent, "Erreur de saisie",
                    "Le nombre de messages par jour doit être entre 1 et 30 !"
                )
                logging.error("Erreur de saisie : Le nombre de messages par jour doit être entre 1 et 30 !")
                return False
            self._messages_per_day_int = value
        except ValueError:
            QMessageBox.warning(
                self.parent, "Erreur de saisie",
                "Le nombre de messages par jour doit être un nombre valide !"
            )
            logging.error("Erreur de saisie : Le nombre de messages par jour doit être un nombre valide !")
            return False

        return True

    def save_configuration(self):
        if self._messages_per_day_int is not None:
            self.config_manager.update({
                'MESSAGES_PER_DAY': self._messages_per_day_int
            })

    def get_messages_per_day_int(self):
        """Retourne la valeur entière validée."""
        return self._messages_per_day_int

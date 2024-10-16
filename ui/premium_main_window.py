# premium_main_window.py

from ui.base_main_window import BaseMainWindow
from ui.premium_features_mixin import PremiumFeaturesMixin


class PremiumMainWindow(PremiumFeaturesMixin, BaseMainWindow):
    def __init__(self):
        super().__init__()

    def setup_ui(self):
        """Configure l'UI pour les utilisateurs premium."""
        super().setup_ui()
        self.setup_premium_ui()

    def start_bot(self):
        """Démarre le bot avec les fonctionnalités premium."""
        if not self.validate_premium_inputs():
            return

        # Sauvegarder la configuration premium
        self.save_premium_configuration()

        # Procéder aux validations et configurations de base
        if not self.validate_inputs():
            return

        self.save_configuration()
        self.run_premium_bot()

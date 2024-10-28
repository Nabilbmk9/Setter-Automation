# standard_main_window.py

from ui.base_main_window import BaseMainWindow

class StandardMainWindow(BaseMainWindow):
    def __init__(self):
        super().__init__()

    def setup_ui(self):
        """Configure l'UI pour les utilisateurs standard."""
        super().setup_ui()

        # Ajouter le bouton Start Bot à la fin pour les utilisateurs standard
        self.setup_start_button()

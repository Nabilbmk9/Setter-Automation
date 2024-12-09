from ui.premium_main_window import PremiumMainWindow
from ui.features.test_mode_feature import TestModeFeature
from ui.features.auto_reply_feature import AutoReplyFeature

class UltimateMainWindow(PremiumMainWindow):
    def __init__(self):
        super().__init__()

        # Initialiser les features Ultimate
        self.test_mode_feature = TestModeFeature(self, self.config_manager)
        self.auto_reply_feature = AutoReplyFeature(self, self.config_manager)

        # Appeler setup_ui() après l'initialisation de toutes les features
        self.setup_ui()

    def setup_ui(self):
        """Configure les éléments Ultimate dans l'ordre souhaité."""
        self.title_feature.setup()
        self.linkedin_credentials_feature.setup()
        self.search_link_feature.setup()
        self.messages_per_day_feature.setup()
        self.message_type_feature.setup()
        self.message_templates_feature.setup()
        self.openai_settings_feature.setup()
        self.profile_analysis_feature.setup()

        self.test_mode_feature.setup()
        self.auto_reply_feature.setup()

        self.setup_start_button()

    def validate_inputs(self):
        """Valide les champs de saisie Ultimate."""
        if not super().validate_inputs():
            return False

        if self.auto_reply_feature.radio_yes.isChecked():
            if not self.auto_reply_feature.validate():
                return False

        return True

    def save_configuration(self):
        """Sauvegarde les données de configuration Ultimate."""
        super().save_configuration()

        self.test_mode_feature.save_configuration()
        self.auto_reply_feature.save_configuration()
        self.config_manager.save()

from ui.base_main_window import BaseMainWindow
from ui.features.message_type_feature import MessageTypeFeature
from ui.features.openai_settings_feature import OpenAISettingsFeature
from ui.features.profile_analysis_feature import ProfileAnalysisFeature


class PremiumMainWindow(BaseMainWindow):
    def __init__(self):
        super().__init__()

        # Initialiser les features Premium
        self.message_type_feature = MessageTypeFeature(self, self.config_manager)
        self.openai_settings_feature = OpenAISettingsFeature(self, self.config_manager, self.message_type_feature)
        self.profile_analysis_feature = ProfileAnalysisFeature(self, self.config_manager, self.message_type_feature)

        # setup_ui() n'est pas appelé ici pour plus de flexibilité

    def setup_ui(self):
        """Configure les éléments Premium dans l'ordre souhaité."""
        # Réutiliser les features de BaseMainWindow
        self.title_feature.setup()
        self.linkedin_credentials_feature.setup()
        self.search_link_feature.setup()

        # Ajouter les features Premium
        self.message_type_feature.setup()
        self.messages_per_day_feature.setup()
        self.message_templates_feature.setup()
        self.openai_settings_feature.setup()
        self.profile_analysis_feature.setup()

        # Ajouter le bouton Start Bot en bas
        self.setup_start_button()

    def toggle_message_fields(self):
        """Afficher ou cacher les widgets en fonction du type de message."""
        if self.message_type_feature.radio_standard.isChecked():
            self.message_templates_feature.show()
            self.openai_settings_feature.hide()
            self.profile_analysis_feature.hide()
        else:
            self.message_templates_feature.hide()
            self.openai_settings_feature.show()
            self.profile_analysis_feature.show()

    def validate_inputs(self):
        """Valide les champs de saisie Premium."""
        # Valider les inputs de BaseMainWindow
        if not super().validate_inputs():
            return False

        # Valider les inputs spécifiques à Premium
        if self.message_type_feature.radio_gpt.isChecked():
            if not self.openai_settings_feature.validate():
                return False
            if not self.profile_analysis_feature.validate():
                return False

        return True

    def save_configuration(self):
        """Sauvegarde les données de configuration Premium."""
        # Sauvegarder les données de BaseMainWindow
        super().save_configuration()

        # Sauvegarder les données spécifiques à Premium
        if self.message_type_feature.radio_gpt.isChecked():
            self.openai_settings_feature.save_configuration()
            self.profile_analysis_feature.save_configuration()

        # Sauvegarder la configuration complète
        self.config_manager.save()

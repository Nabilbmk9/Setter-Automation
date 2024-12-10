from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QStackedWidget
from PySide6.QtGui import QIcon
from config.configuration_manager import ConfigurationManager
from ui.features.title_feature import TitleFeature
from ui.features.linkedin_credentials_feature import LinkedInCredentialsFeature
from ui.features.search_link_feature import SearchLinkFeature
from ui.features.messages_per_day_feature import MessagesPerDayFeature
from ui.features.message_type_feature import MessageTypeFeature
from ui.features.openai_settings_feature import OpenAISettingsFeature
from ui.features.profile_analysis_feature import ProfileAnalysisFeature
from ui.features.test_mode_feature import TestModeFeature
from ui.features.auto_reply_feature import AutoReplyFeature
from utils.utils import get_resource_path
from ui.styles import get_stylesheet
from ui.message_config_page import MessageConfigPage
from ui.ia_config_page import IAConfigPage


class UltimateMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigurationManager()

        self.setWindowTitle("Bot LinkedIn Ultimate")
        self.setWindowIcon(QIcon(get_resource_path("ui/resources/logo3d.png")))
        self.setStyleSheet(get_stylesheet())

        # Gestionnaire de pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Pages
        self.main_page = QWidget()  # Contient les fonctionnalités principales
        self.message_config_page = MessageConfigPage(config_manager=self.config_manager, parent=self)  # Inclut la gestion des messages
        self.ia_config_page = IAConfigPage()

        # Ajout des pages au QStackedWidget
        self.stacked_widget.addWidget(self.main_page)           # index 0
        self.stacked_widget.addWidget(self.message_config_page) # index 1
        self.stacked_widget.addWidget(self.ia_config_page)      # index 2

        # Initialisation de la page principale
        self.main_layout = QVBoxLayout()
        self.main_page.setLayout(self.main_layout)
        self.init_main_page_features()

        # Connexions entre les pages
        self.message_config_page.btn_enregistrer.clicked.connect(self.save_message_config)
        self.message_config_page.btn_annuler.clicked.connect(self.cancel_message_config)
        self.ia_config_page.btn_enregistrer.clicked.connect(self.save_ia_config)
        self.ia_config_page.btn_annuler.clicked.connect(self.cancel_ia_config)

    def init_main_page_features(self):
        """Initialise les fonctionnalités principales."""
        # Initialiser toutes les features
        self.title_feature = TitleFeature(self, self.config_manager)
        self.linkedin_credentials_feature = LinkedInCredentialsFeature(self, self.config_manager)
        self.search_link_feature = SearchLinkFeature(self, self.config_manager)
        self.messages_per_day_feature = MessagesPerDayFeature(self, self.config_manager)
        self.message_type_feature = MessageTypeFeature(self, self.config_manager)
        self.openai_settings_feature = OpenAISettingsFeature(self, self.config_manager, self.message_type_feature)
        self.profile_analysis_feature = ProfileAnalysisFeature(self, self.config_manager, self.message_type_feature)
        self.test_mode_feature = TestModeFeature(self, self.config_manager)
        self.auto_reply_feature = AutoReplyFeature(self, self.config_manager)

        # Ajouter les widgets au layout principal
        self.title_feature.setup()
        self.linkedin_credentials_feature.setup()
        self.search_link_feature.setup()
        self.messages_per_day_feature.setup()
        self.message_type_feature.setup()
        self.openai_settings_feature.setup()
        self.profile_analysis_feature.setup()
        self.test_mode_feature.setup()
        self.auto_reply_feature.setup()

        # Ajouter les boutons de navigation
        self.btn_configurer_messages = QPushButton("Configurer les messages")
        self.btn_configurer_messages.clicked.connect(self.goto_message_config)
        self.main_layout.addWidget(self.btn_configurer_messages)

        self.btn_configurer_ia = QPushButton("Configurer l'IA")
        self.btn_configurer_ia.clicked.connect(self.goto_ia_config)
        self.main_layout.addWidget(self.btn_configurer_ia)

        self.setup_start_button()

    def setup_start_button(self):
        """Ajoute le bouton de démarrage."""
        self.start_button = QPushButton("Start Bot")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self.start_bot)
        self.main_layout.addWidget(self.start_button)

    def goto_message_config(self):
        """Navigue vers la page de configuration des messages."""
        self.stacked_widget.setCurrentIndex(1)

    def cancel_message_config(self):
        """Annule la configuration des messages et retourne à la page principale."""
        self.stacked_widget.setCurrentIndex(0)

    def save_message_config(self):
        """Sauvegarde la configuration des messages et retourne à la page principale."""
        self.message_config_page.save_configuration()
        self.stacked_widget.setCurrentIndex(0)

    def goto_ia_config(self):
        """Navigue vers la page de configuration de l'IA."""
        self.stacked_widget.setCurrentIndex(2)

    def cancel_ia_config(self):
        """Annule la configuration de l'IA et retourne à la page principale."""
        self.stacked_widget.setCurrentIndex(0)

    def save_ia_config(self):
        """Sauvegarde la configuration de l'IA et retourne à la page principale."""
        self.stacked_widget.setCurrentIndex(0)

    def validate_inputs(self):
        """Valide les champs Ultimate."""
        if self.message_type_feature.radio_gpt.isChecked():
            if not self.openai_settings_feature.validate():
                return False
            if not self.profile_analysis_feature.validate():
                return False
        if self.auto_reply_feature.radio_yes.isChecked():
            if not self.auto_reply_feature.validate():
                return False
        return True

    def save_configuration(self):
        """Sauvegarde les données de configuration Ultimate."""
        self.config_manager.save()
        self.test_mode_feature.save_configuration()
        self.auto_reply_feature.save_configuration()

    def start_bot(self):
        """Lance le bot si les données sont valides."""
        if not self.validate_inputs():
            return
        self.save_configuration()
        print("Bot démarré")

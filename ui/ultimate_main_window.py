from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QStackedWidget, QLabel, QRadioButton, QButtonGroup
from PySide6.QtGui import QIcon, QGuiApplication
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
from ui.features.message_templates_feature import MessageTemplatesFeature
from ui.features.prospecting_assistant_feature import ProspectingAssistantFeature
from ui.styles import get_stylesheet
from ui.message_config_page import MessageConfigPage
from ui.ia_config_page import IAConfigPage
from utils.utils import get_resource_path


class UltimateMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigurationManager()

        self.setWindowTitle("Bot LinkedIn Ultimate")
        self.setWindowIcon(QIcon(get_resource_path("ui/resources/logo3d.png")))
        self.setStyleSheet(get_stylesheet())

        # Fixer la taille de la fenêtre
        self.setFixedSize(400, 850)  # Largeur : 800px, Hauteur : 600px

        self.position_window()

        # Encapsulation dans un widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal pour le central widget avec des marges
        self.central_layout = QVBoxLayout()
        self.central_layout.setContentsMargins(15, 5, 15, 15)  # Marges : gauche, haut, droite, bas
        central_widget.setLayout(self.central_layout)

        # Gestionnaire de pages
        self.stacked_widget = QStackedWidget()
        self.central_layout.addWidget(self.stacked_widget)

        # Création des features nécessaires (une seule fois)
        self.message_type_feature = MessageTypeFeature(self, self.config_manager)
        self.openai_settings_feature = OpenAISettingsFeature(self, self.config_manager)
        self.prospecting_assistant_feature = ProspectingAssistantFeature(self, self.config_manager)
        self.message_templates_feature = MessageTemplatesFeature(self, self.config_manager)
        self.test_mode_feature = TestModeFeature(self, self.config_manager)
        self.auto_reply_feature = AutoReplyFeature(self, self.config_manager)
        self.profile_analysis_feature = ProfileAnalysisFeature(self, self.config_manager)

        # Pages
        self.main_page = QWidget()
        self.message_config_page = MessageConfigPage(
            message_templates_feature=self.message_templates_feature,
            parent=self
        )
        self.ia_config_page = IAConfigPage(
            openai_settings_feature=self.openai_settings_feature,
            test_mode_feature=self.test_mode_feature,
            auto_reply_feature=self.auto_reply_feature,
            profile_analysis_feature=self.profile_analysis_feature,
            config_manager=self.config_manager,
            parent=self
        )

        self.stacked_widget.addWidget(self.main_page)           # index 0
        self.stacked_widget.addWidget(self.message_config_page) # index 1
        self.stacked_widget.addWidget(self.ia_config_page)      # index 2

        self.main_layout = QVBoxLayout()
        self.main_page.setLayout(self.main_layout)
        self.init_main_page_features()

        self.message_config_page.btn_enregistrer.clicked.connect(self.save_message_config)
        self.message_config_page.btn_annuler.clicked.connect(self.cancel_message_config)
        self.ia_config_page.btn_enregistrer.clicked.connect(self.save_ia_config)
        self.ia_config_page.btn_annuler.clicked.connect(self.cancel_ia_config)

    def position_window(self):
        """Positionne la fenêtre au centre en haut de l'écran avec une marge."""
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()

        # Dimensions de l'écran
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Dimensions de la fenêtre
        window_width = self.frameGeometry().width()  # Utiliser la taille réelle de la fenêtre, y compris les bordures
        window_height = self.frameGeometry().height()

        # Calcul des coordonnées
        x = (screen_width - window_width) // 2  # Centrer la fenêtre horizontalement
        y = 20  # Petite marge depuis le haut

        self.move(x, y)

    def init_main_page_features(self):
        self.title_feature = TitleFeature(self, self.config_manager)
        self.linkedin_credentials_feature = LinkedInCredentialsFeature(self, self.config_manager)
        self.search_link_feature = SearchLinkFeature(self, self.config_manager)
        self.messages_per_day_feature = MessagesPerDayFeature(self, self.config_manager)

        self.title_feature.setup()
        self.linkedin_credentials_feature.setup()
        self.search_link_feature.setup()
        self.messages_per_day_feature.setup()

        type_label = QLabel("Type de message à envoyer :")
        self.main_layout.addWidget(type_label)

        self.radio_button_group = QButtonGroup(self)
        self.radio_message_normal = QRadioButton("Messages normaux")
        self.radio_message_custom = QRadioButton("Messages personnalisés")
        self.radio_button_group.addButton(self.radio_message_normal)
        self.radio_button_group.addButton(self.radio_message_custom)

        self.main_layout.addWidget(self.radio_message_normal)
        self.main_layout.addWidget(self.radio_message_custom)

        # Connecter les événements
        self.radio_message_normal.toggled.connect(self.update_configure_message_button_visibility)
        self.radio_message_custom.toggled.connect(self.update_configure_ia_button_visibility)
        self.profile_analysis_feature.analysis_yes_radio.toggled.connect(self.update_configure_ia_button_visibility)
        self.auto_reply_feature.auto_reply_yes_radio.toggled.connect(self.update_configure_ia_button_visibility)
        self.auto_reply_feature.auto_reply_no_radio.toggled.connect(self.update_configure_ia_button_visibility)

        self.btn_configurer_messages = QPushButton("Configurer les messages")
        self.btn_configurer_messages.setObjectName("btnConfig")
        self.btn_configurer_messages.clicked.connect(self.goto_message_config)
        self.main_layout.addWidget(self.btn_configurer_messages)

        self.profile_analysis_feature.setup()
        self.auto_reply_feature.setup()

        self.btn_configurer_ia = QPushButton("Configurer l'IA")
        self.btn_configurer_ia.setObjectName("btnConfig")
        self.btn_configurer_ia.clicked.connect(self.goto_ia_config)
        self.main_layout.addWidget(self.btn_configurer_ia)

        self.update_configure_message_button_visibility()
        self.update_configure_ia_button_visibility()

        self.setup_start_button()

    def update_configure_message_button_visibility(self):
        self.btn_configurer_messages.setVisible(self.radio_message_normal.isChecked())

    def update_configure_ia_button_visibility(self):
        show_configure_ia = (
            self.radio_message_custom.isChecked() or
            self.profile_analysis_feature.is_analysis_enabled() or
            self.auto_reply_feature.is_auto_reply_enabled()
        )
        self.btn_configurer_ia.setVisible(show_configure_ia)

        # Mise à jour des champs dans la page IA
        self.ia_config_page.update_prospecting_fields(self.radio_message_custom.isChecked())

    def goto_message_config(self):
        self.stacked_widget.setCurrentIndex(1)

    def cancel_message_config(self):
        self.stacked_widget.setCurrentIndex(0)

    def save_message_config(self):
        self.message_config_page.save_configuration()
        self.stacked_widget.setCurrentIndex(0)

    def goto_ia_config(self):
        # Mettre à jour les champs avant d'afficher la page
        self.ia_config_page.update_auto_reply_fields()
        self.ia_config_page.update_analysis_fields()
        self.stacked_widget.setCurrentIndex(2)

    def cancel_ia_config(self):
        self.stacked_widget.setCurrentIndex(0)

    def save_ia_config(self):
        self.ia_config_page.save_configuration()
        self.stacked_widget.setCurrentIndex(0)

    def validate_inputs(self):
        # Validation standard si besoin
        return True

    def save_configuration(self):
        self.config_manager.save()
        self.test_mode_feature.save_configuration()
        self.auto_reply_feature.save_configuration()
        self.profile_analysis_feature.save_configuration()

    def setup_start_button(self):
        self.start_button = QPushButton("Start Bot")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self.start_bot)
        self.main_layout.addWidget(self.start_button)

    def start_bot(self):
        if not self.validate_inputs():
            return
        self.save_configuration()
        print("Bot démarré")

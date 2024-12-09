from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton
from PySide6.QtGui import QIcon
from config.configuration_manager import ConfigurationManager
from ui.features.title_feature import TitleFeature
from ui.features.linkedin_credentials_feature import LinkedInCredentialsFeature
from ui.features.search_link_feature import SearchLinkFeature
from ui.features.messages_per_day_feature import MessagesPerDayFeature
from ui.features.message_templates_feature import MessageTemplatesFeature
from utils.utils import get_resource_path
from ui.styles import get_stylesheet

class BaseMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigurationManager()

        self.setWindowTitle("Bot LinkedIn")
        self.setWindowIcon(QIcon(get_resource_path("ui/resources/logo3d.png")))
        self.setStyleSheet(get_stylesheet())

        self.main_layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        # Définir les features standard sans appeler setup_ui() ici
        self.title_feature = TitleFeature(self, self.config_manager)
        self.linkedin_credentials_feature = LinkedInCredentialsFeature(self, self.config_manager)
        self.search_link_feature = SearchLinkFeature(self, self.config_manager)
        self.messages_per_day_feature = MessagesPerDayFeature(self, self.config_manager)
        self.message_templates_feature = MessageTemplatesFeature(self, self.config_manager)

    def setup_ui(self):
        """Appelé par les classes enfant après avoir défini toutes leurs features."""
        self.title_feature.setup()
        self.linkedin_credentials_feature.setup()
        self.search_link_feature.setup()
        self.messages_per_day_feature.setup()
        self.message_templates_feature.setup()

        self.setup_start_button()

    def setup_start_button(self):
        self.start_button = QPushButton("Start Bot")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self.start_bot)
        self.main_layout.addWidget(self.start_button)

    def validate_inputs(self):
        # Validation standard
        return True

    def save_configuration(self):
        # Sauvegarde standard
        self.config_manager.save()

    def start_bot(self):
        if not self.validate_inputs():
            return
        self.save_configuration()
        print("Bot démarré")

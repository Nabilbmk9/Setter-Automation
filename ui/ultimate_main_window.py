import logging

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QStackedWidget, QLabel, QRadioButton, \
    QButtonGroup, QMessageBox
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
            config_manager=self.config_manager,
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
        self.message_type_feature.setup()

        self.btn_configurer_messages = QPushButton("Configurer les messages à envoyer")
        self.btn_configurer_messages.setObjectName("btnConfig")
        self.btn_configurer_messages.clicked.connect(self.goto_message_config)
        self.main_layout.addWidget(self.btn_configurer_messages)

        # Initialisation de l'analyse de profil et auto-réponse
        self.profile_analysis_feature.setup()
        self.auto_reply_feature.setup()

        # Connexions pour mettre à jour l'affichage en fonction du type de message, de l'analyse, etc.
        self.message_type_feature.normal_message_radio.toggled.connect(self.update_configure_message_button_visibility)
        self.message_type_feature.chatgpt_message_radio.toggled.connect(self.update_configure_ia_button_visibility)
        self.profile_analysis_feature.analysis_yes_radio.toggled.connect(self.update_configure_ia_button_visibility)
        self.auto_reply_feature.auto_reply_yes_radio.toggled.connect(self.update_configure_ia_button_visibility)
        self.auto_reply_feature.auto_reply_no_radio.toggled.connect(self.update_configure_ia_button_visibility)

        self.btn_configurer_ia = QPushButton("Configurer les parametres chatGPT")
        self.btn_configurer_ia.setObjectName("btnConfig")
        self.btn_configurer_ia.clicked.connect(self.goto_ia_config)
        self.main_layout.addWidget(self.btn_configurer_ia)

        self.update_configure_message_button_visibility()
        self.update_configure_ia_button_visibility()

        self.setup_start_button()

    def update_configure_message_button_visibility(self):
        # Le bouton de configuration des messages standard n'est visible que si l'on n'utilise pas ChatGPT
        self.btn_configurer_messages.setVisible(not self.message_type_feature.is_chatgpt_selected())

    def update_configure_ia_button_visibility(self):
        show_configure_ia = (
                self.message_type_feature.is_chatgpt_selected() or
                self.profile_analysis_feature.is_analysis_enabled() or
                self.auto_reply_feature.is_auto_reply_enabled()
        )
        self.btn_configurer_ia.setVisible(show_configure_ia)

        # Mise à jour des champs dans la page IA
        self.ia_config_page.update_prospecting_fields(self.message_type_feature.is_chatgpt_selected())
        self.test_mode_feature.set_enabled_based_on_message_type(self.message_type_feature.is_chatgpt_selected())

    def goto_message_config(self):
        # Recharger la configuration avant d'afficher la page
        self.message_templates_feature.reload_configuration()
        self.stacked_widget.setCurrentIndex(1)

    def cancel_message_config(self):
        self.stacked_widget.setCurrentIndex(0)

    def save_message_config(self):
        if not self.message_config_page.save_configuration():
            return
        self.stacked_widget.setCurrentIndex(0)

    def goto_ia_config(self):
        # Recharger la configuration avant d'afficher la page IA
        self.ia_config_page.reload_configuration()
        self.stacked_widget.setCurrentIndex(2)

    def cancel_ia_config(self):
        self.stacked_widget.setCurrentIndex(0)

    def save_ia_config(self):
        if self.ia_config_page.save_configuration():
            self.stacked_widget.setCurrentIndex(0)

    def validate_inputs(self):
        # Liste des validations
        validations = [
            self.linkedin_credentials_feature.validate,
            self.search_link_feature.validate,
            self.messages_per_day_feature.validate,
            self.message_templates_feature.validate
        ]
        for validate in validations:
            if not validate():
                return False
        return True

    def save_configuration(self):
        self.linkedin_credentials_feature.save_configuration()
        self.messages_per_day_feature.save_configuration()
        self.search_link_feature.save_configuration()
        self.test_mode_feature.save_configuration()
        self.auto_reply_feature.save_configuration()
        self.profile_analysis_feature.save_configuration()

        # Sauvegarde du type de message via le message_type_feature
        self.message_type_feature.save_configuration()

        self.config_manager.save()

    def setup_start_button(self):
        self.start_button = QPushButton("Start Bot")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self.start_bot)
        self.main_layout.addWidget(self.start_button)

    def start_bot(self):
        if not self.validate_inputs():
            return

        # Sauvegarder la configuration
        self.save_configuration()

        # Récupérer les données depuis le config_manager
        username = self.config_manager.get('LINKEDIN_EMAIL', '')
        password = self.config_manager.get('LINKEDIN_PASSWORD', '')
        search_link = self.config_manager.get('LINKEDIN_SEARCH_LINK', '')
        messages_per_day = self.config_manager.get('MESSAGES_PER_DAY', 20)
        message_a = self.config_manager.get('MESSAGE_A', '')
        message_b = self.config_manager.get('MESSAGE_B', '')

        # Déterminer le type de message
        message_type = 'custom' if self.message_type_feature.chatgpt_message_radio.isChecked() else 'normal'

        analyze_profiles = self.profile_analysis_feature.is_analysis_enabled()
        relevance_prompt = self.config_manager.get('RELEVANCE_PROMPT', '') if analyze_profiles else None

        auto_reply_enabled = self.auto_reply_feature.is_auto_reply_enabled()
        auto_reply_assistant_id = self.config_manager.get('AUTO_REPLY_ASSISTANT_ID', '')
        prospecting_assistant_id = self.config_manager.get('PROSPECTING_ASSISTANT_ID', '')
        test_mode_enabled = self.config_manager.get('TEST_MODE_ENABLED', False)

        openai_api_key = self.config_manager.get('OPENAI_API_KEY', '')

        # Instancier le ChatGPTManager si nécessaire
        chatgpt_manager = None
        if message_type == 'custom' or analyze_profiles or auto_reply_enabled:
            # Import adapter en fonction de votre structure de projet
            from services.chatgpt_manager import ChatGPTManager
            chatgpt_manager = ChatGPTManager(
                api_key=openai_api_key,
                relevance_prompt_template=relevance_prompt
            )

        # Importer MainController (adapter le chemin selon votre structure)
        from controllers.main_controller import MainController

        controller = MainController(
            username=username,
            password=password,
            search_link=search_link,
            messages_per_day=messages_per_day,
            message_a=message_a,
            message_b=message_b,
            chatgpt_manager=chatgpt_manager,
            message_type='chatgpt' if message_type == 'custom' else message_type,
            analyze_profiles=analyze_profiles,
            auto_reply_enabled=auto_reply_enabled,
            auto_reply_assistant_id=auto_reply_assistant_id,
            prospecting_assistant_id=prospecting_assistant_id,
            test_mode_enabled=test_mode_enabled
        )

        # Optionnel : Vérifier la limite quotidienne
        # Cette logique suppose que data_manager est accessible via controller
        limit_reached, messages_sent = controller.data_manager.has_reached_message_limit(messages_per_day)
        if limit_reached and not auto_reply_enabled:
            QMessageBox.warning(
                self, "Limite atteinte",
                f"Le bot a déjà envoyé le nombre maximum de messages aujourd'hui ({messages_sent}/{messages_per_day})."
            )
            return

        # Démarrer le bot
        try:
            controller.run()
            if auto_reply_enabled:
                QMessageBox.information(
                    self, "Bot en cours d'exécution",
                    "Le bot a terminé l'envoi des messages de prospection.\n"
                    "Il continue à gérer les réponses automatiques.\n"
                    "Vous pouvez fermer l'application pour arrêter le bot."
                )
            else:
                QMessageBox.information(self, "Fin du bot", "Le bot a terminé son exécution.")
        except Exception as e:
            logging.error(f"Erreur lors de l'exécution du bot: {e}")
            QMessageBox.critical(self, "Erreur critique", f"Une erreur est survenue : {e}")


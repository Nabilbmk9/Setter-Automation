# ia_config_page.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QMessageBox, QHBoxLayout
from ui.features.prospecting_assistant_feature import ProspectingAssistantFeature
from ui.features.title_feature import TitleFeature

class IAConfigPage(QWidget):
    def __init__(self, openai_settings_feature, test_mode_feature, auto_reply_feature, profile_analysis_feature, config_manager, parent=None):
        super().__init__(parent)
        self.openai_settings_feature = openai_settings_feature
        self.test_mode_feature = test_mode_feature
        self.auto_reply_feature = auto_reply_feature
        self.profile_analysis_feature = profile_analysis_feature
        self.config_manager = config_manager

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(15, 5, 15, 15)

        self.title_feature = TitleFeature(self, config_manager)
        self.title_feature.add_to_layout(self.layout)

        subtitle_label = QLabel("Configuration des parametres chatGPT")
        subtitle_label.setObjectName("subtitle")
        self.layout.addWidget(subtitle_label)

        self.prospecting_assistant_feature = ProspectingAssistantFeature(self, config_manager)

        self.relevance_prompt_label = QLabel("Prompt pour l'analyse des profils:")
        self.relevance_prompt_input = QTextEdit()

        self.auto_reply_assistant_id_label = QLabel("Assistant ID pour les réponses automatiques:")
        self.auto_reply_assistant_id_input = QLineEdit()

        self.btn_enregistrer = QPushButton("Enregistrer")
        self.btn_annuler = QPushButton("Annuler")

        self.btn_enregistrer.setObjectName("btnEnregistrer")
        self.btn_annuler.setObjectName("btnAnnuler")

        self.layout.addLayout(self.openai_settings_feature.layout)
        self.layout.addLayout(self.prospecting_assistant_feature.layout)
        self.layout.addLayout(self.prospecting_assistant_feature.layout)

        self.layout.addWidget(self.auto_reply_assistant_id_label)
        self.layout.addWidget(self.auto_reply_assistant_id_input)

        self.layout.addWidget(self.relevance_prompt_label)
        self.layout.addWidget(self.relevance_prompt_input)

        self.layout.addLayout(self.test_mode_feature.layout)

        self.buttons_layout = QHBoxLayout()
        self.layout.addStretch()
        self.buttons_layout.addWidget(self.btn_enregistrer)
        self.buttons_layout.addWidget(self.btn_annuler)
        self.layout.addLayout(self.buttons_layout)

        self.setLayout(self.layout)

        self.btn_enregistrer.clicked.connect(self.save_configuration)

        # Par défaut, caché
        self.auto_reply_assistant_id_label.setVisible(False)
        self.auto_reply_assistant_id_input.setVisible(False)
        self.relevance_prompt_label.setVisible(False)
        self.relevance_prompt_input.setVisible(False)

    def update_prospecting_fields(self, is_custom_message_selected):
        self.prospecting_assistant_feature.assistant_id_label.setVisible(is_custom_message_selected)
        self.prospecting_assistant_feature.assistant_id_input.setVisible(is_custom_message_selected)

    def update_auto_reply_fields(self):
        enabled = self.auto_reply_feature.is_auto_reply_enabled()
        self.auto_reply_assistant_id_label.setVisible(enabled)
        self.auto_reply_assistant_id_input.setVisible(enabled)
        if enabled:
            self.auto_reply_assistant_id_input.setText(self.auto_reply_feature.get_assistant_id())

    def update_analysis_fields(self):
        enabled = self.profile_analysis_feature.is_analysis_enabled()
        self.relevance_prompt_label.setVisible(enabled)
        self.relevance_prompt_input.setVisible(enabled)
        if enabled:
            self.relevance_prompt_input.setText(self.config_manager.get('RELEVANCE_PROMPT', ''))

    def validate(self):
        # On récupère juste les booléens depuis les features sans afficher de message
        if self.profile_analysis_feature.is_analysis_enabled() and not self.relevance_prompt_input.toPlainText().strip():
            return False
        if self.auto_reply_feature.is_auto_reply_enabled() and not self.auto_reply_assistant_id_input.text().strip():
            return False
        if not self.openai_settings_feature.validate():  # suppose qu'elle retourne True ou False
            return False
        if not self.test_mode_feature.validate():
            return False
        if not self.prospecting_assistant_feature.validate():
            return False
        return True

    def save_configuration(self):
        if not self.validate():
            QMessageBox.warning(self, "Erreur de saisie", "Veuillez remplir tous les champs requis.")
            return False

        self.openai_settings_feature.save_configuration()
        self.test_mode_feature.save_configuration()
        self.prospecting_assistant_feature.save_configuration()

        if self.auto_reply_feature.is_auto_reply_enabled():
            self.config_manager.update({'AUTO_REPLY_ASSISTANT_ID': self.auto_reply_assistant_id_input.text().strip()})

        if self.profile_analysis_feature.is_analysis_enabled():
            self.config_manager.update({'RELEVANCE_PROMPT': self.relevance_prompt_input.toPlainText().strip()})

        self.config_manager.save()
        return True

    def reload_configuration(self):
        # Recharger les valeurs depuis la config
        self.prospecting_assistant_feature.assistant_id_input.setText(self.config_manager.get('PROSPECTING_ASSISTANT_ID', ''))
        self.update_auto_reply_fields()
        self.update_analysis_fields()
        # Recharger openai_settings_feature, test_mode_feature si nécessaire
        self.openai_settings_feature.reload_configuration()
        self.test_mode_feature.reload_configuration()

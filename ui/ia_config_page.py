from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QMessageBox


class IAConfigPage(QWidget):
    def __init__(self, openai_settings_feature, test_mode_feature, auto_reply_feature, profile_analysis_feature, config_manager, parent=None):
        super().__init__(parent)
        self.openai_settings_feature = openai_settings_feature
        self.test_mode_feature = test_mode_feature
        self.auto_reply_feature = auto_reply_feature
        self.profile_analysis_feature = profile_analysis_feature
        self.config_manager = config_manager

        # Widgets pour l'Assistant ID des réponses automatiques
        self.auto_reply_assistant_id_label = QLabel("Assistant ID pour les réponses automatiques:")
        self.auto_reply_assistant_id_input = QLineEdit()

        # Widgets pour le prompt d'analyse des profils
        self.relevance_prompt_label = QLabel("Prompt pour l'analyse des profils:")
        self.relevance_prompt_input = QTextEdit()

        # Boutons Enregistrer et Annuler
        self.btn_enregistrer = QPushButton("Enregistrer")
        self.btn_annuler = QPushButton("Annuler")

        # Layout principal
        self.layout = QVBoxLayout()

        # Intégrer les layouts d'OpenAISettingsFeature et TestModeFeature
        self.layout.addLayout(self.openai_settings_feature.layout)
        self.layout.addWidget(self.test_mode_feature.test_mode_checkbox)

        # Ajouter les widgets "Assistant ID pour les réponses automatiques"
        self.layout.addWidget(self.auto_reply_assistant_id_label)
        self.layout.addWidget(self.auto_reply_assistant_id_input)

        # Ajouter les widgets "Prompt pour l'analyse des profils"
        self.layout.addWidget(self.relevance_prompt_label)
        self.layout.addWidget(self.relevance_prompt_input)

        # Ajouter les boutons au layout
        self.layout.addWidget(self.btn_enregistrer)
        self.layout.addWidget(self.btn_annuler)

        self.setLayout(self.layout)

        # Connexions
        self.btn_enregistrer.clicked.connect(self.save_configuration)
        self.auto_reply_assistant_id_label.setVisible(False)
        self.auto_reply_assistant_id_input.setVisible(False)
        self.relevance_prompt_label.setVisible(False)
        self.relevance_prompt_input.setVisible(False)

    def update_analysis_fields(self):
        """Met à jour la visibilité des widgets de l'analyse des profils."""
        visible = self.profile_analysis_feature.is_analysis_enabled()
        self.relevance_prompt_label.setVisible(visible)
        self.relevance_prompt_input.setVisible(visible)
        if visible:
            self.relevance_prompt_input.setText(self.config_manager.get('RELEVANCE_PROMPT', ''))

    def update_auto_reply_fields(self):
        """Met à jour la visibilité des widgets de l'Assistant ID."""
        enabled = self.auto_reply_feature.is_auto_reply_enabled()
        self.auto_reply_assistant_id_label.setVisible(enabled)
        self.auto_reply_assistant_id_input.setVisible(enabled)
        if enabled:
            self.auto_reply_assistant_id_input.setText(self.auto_reply_feature.get_assistant_id())

    def validate(self):
        """Valide les paramètres OpenAI, le mode test, les réponses automatiques et l'analyse des profils."""
        if self.profile_analysis_feature.is_analysis_enabled():
            if not self.relevance_prompt_input.toPlainText().strip():
                QMessageBox.warning(self, "Erreur de saisie", "Veuillez entrer un prompt pour l'analyse des profils.")
                return False
        if self.auto_reply_feature.is_auto_reply_enabled():
            if not self.auto_reply_assistant_id_input.text().strip():
                QMessageBox.warning(self, "Erreur de saisie", "Veuillez entrer l'Assistant ID pour les réponses automatiques.")
                return False
        return self.openai_settings_feature.validate()

    def save_configuration(self):
        """Sauvegarde les paramètres OpenAI, le mode test, les réponses automatiques et l'analyse des profils."""
        if self.validate():
            self.openai_settings_feature.save_configuration()
            self.test_mode_feature.save_configuration()
            if self.auto_reply_feature.is_auto_reply_enabled():
                self.config_manager.update({
                    'AUTO_REPLY_ASSISTANT_ID': self.auto_reply_assistant_id_input.text().strip()
                })
            if self.profile_analysis_feature.is_analysis_enabled():
                self.config_manager.update({
                    'RELEVANCE_PROMPT': self.relevance_prompt_input.toPlainText().strip()
                })

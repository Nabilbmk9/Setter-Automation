# ui/features/profile_analysis_feature.py

from PySide6.QtWidgets import QLabel, QCheckBox, QTextEdit, QMessageBox


class ProfileAnalysisFeature:
    def __init__(self, parent, config_manager, message_type_feature):
        self.parent = parent
        self.config_manager = config_manager
        self.message_type_feature = message_type_feature

        self.analyze_profiles_checkbox = QCheckBox("Analyser les profils avant d'envoyer les messages")
        analyze_profiles = self.config_manager.get('ANALYZE_PROFILES', False)
        self.analyze_profiles_checkbox.setChecked(analyze_profiles)

        self.relevance_prompt_label = QLabel("Prompt pour l'analyse des profils:")
        self.relevance_prompt_input = QTextEdit(self.config_manager.get('RELEVANCE_PROMPT', ''))

    def setup(self):
        self.parent.main_layout.addWidget(self.analyze_profiles_checkbox)
        self.parent.main_layout.addWidget(self.relevance_prompt_label)
        self.parent.main_layout.addWidget(self.relevance_prompt_input)

        # Afficher/masquer selon l'état du checkbox
        self.toggle_relevance_prompt()
        self.analyze_profiles_checkbox.stateChanged.connect(self.toggle_relevance_prompt)

    def toggle_relevance_prompt(self):
        visible = self.analyze_profiles_checkbox.isChecked() and self.message_type_feature.is_chatgpt_selected()
        self.relevance_prompt_label.setVisible(visible)
        self.relevance_prompt_input.setVisible(visible)

    def validate(self):
        # Valider seulement si ChatGPT est sélectionné et l'analyse de profil est activée
        if self.analyze_profiles_checkbox.isChecked() and self.message_type_feature.is_chatgpt_selected():
            if not self.relevance_prompt_input.toPlainText().strip():
                QMessageBox.warning(self.parent, "Erreur de saisie", "Veuillez remplir le prompt d'analyse des profils.")
                return False
        return True

    def save_configuration(self):
        analyze_profiles = self.analyze_profiles_checkbox.isChecked()
        self.config_manager.update({
            'ANALYZE_PROFILES': analyze_profiles,
            'RELEVANCE_PROMPT': self.relevance_prompt_input.toPlainText().strip()
        })

from PySide6.QtWidgets import QLabel, QRadioButton, QButtonGroup

class ProfileAnalysisFeature:
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager

        self.analysis_label = QLabel("Voulez-vous analyser les profils avant d'envoyer les messages ?")

        self.analysis_yes_radio = QRadioButton("Oui")
        self.analysis_no_radio = QRadioButton("Non")

        self.analysis_group = QButtonGroup(self.parent)
        self.analysis_group.addButton(self.analysis_yes_radio)
        self.analysis_group.addButton(self.analysis_no_radio)

        analyze_profiles = self.config_manager.get('ANALYZE_PROFILES', False)
        if analyze_profiles:
            self.analysis_yes_radio.setChecked(True)
        else:
            self.analysis_no_radio.setChecked(True)

    def setup(self):
        self.parent.main_layout.addWidget(self.analysis_label)
        self.parent.main_layout.addWidget(self.analysis_yes_radio)
        self.parent.main_layout.addWidget(self.analysis_no_radio)

    def is_analysis_enabled(self):
        return self.analysis_yes_radio.isChecked()

    def save_configuration(self):
        analyze_profiles = self.analysis_yes_radio.isChecked()
        self.config_manager.update({'ANALYZE_PROFILES': analyze_profiles})

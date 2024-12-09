# ui/features/test_mode_feature.py

from PySide6.QtWidgets import QCheckBox


class TestModeFeature:
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager

        self.test_mode_checkbox = QCheckBox("Activer le mode test")
        test_mode_enabled = self.config_manager.get('TEST_MODE_ENABLED', False)
        self.test_mode_checkbox.setChecked(test_mode_enabled)

    def setup(self):
        self.parent.main_layout.addWidget(self.test_mode_checkbox)

    def validate(self):
        return True  # Pas de validation spécifique

    def save_configuration(self):
        self.config_manager.update({
            'TEST_MODE_ENABLED': self.test_mode_checkbox.isChecked()
        })

    def is_test_mode_enabled(self):
        return self.test_mode_checkbox.isChecked()

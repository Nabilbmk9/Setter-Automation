# ui/features/search_link_feature.py

from PySide6.QtWidgets import QLabel, QLineEdit, QMessageBox


class SearchLinkFeature:
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager

        self.search_link_label = QLabel("Lien de recherche:")
        self.search_link_input = QLineEdit(self.config_manager.get('LINKEDIN_SEARCH_LINK', ''))

    def setup(self):
        self.parent.main_layout.addWidget(self.search_link_label)
        self.parent.main_layout.addWidget(self.search_link_input)

    def validate(self):
        search_link = self.search_link_input.text().strip()
        if not search_link:
            QMessageBox.warning(self.parent, "Erreur de saisie", "Le lien de recherche ne peut pas être vide !")
            return False
        return True

    def save_configuration(self):
        self.config_manager.update({
            'LINKEDIN_SEARCH_LINK': self.search_link_input.text().strip()
        })

    def get_search_link(self):
        return self.search_link_input.text().strip()

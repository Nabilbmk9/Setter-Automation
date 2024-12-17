from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QRadioButton, QButtonGroup
from ui.message_edit_dialog import MessageEditDialog


class MessageTemplatesFeature:
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager

        self.message_a_text = self.config_manager.get('MESSAGE_A', '')
        self.message_b_text = self.config_manager.get('MESSAGE_B', '')
        self.use_ab_testing = self.config_manager.get('USE_AB_TESTING', False)

        self.message_a_label = QLabel("Message Template A:")
        self.message_a_label.setObjectName("messageConfig")
        self.message_a_button = QPushButton(self.get_message_preview(self.message_a_text))
        self.message_a_button.clicked.connect(self.edit_message_a)

        # Question pour l'A/B testing
        self.ab_label = QLabel("Voulez-vous envoyer deux variantes de message grâce à l'A/B testing ?")
        self.ab_label.setObjectName("messageConfig")
        self.ab_label.setWordWrap(True)

        # Boutons Oui/Non
        self.ab_yes = QRadioButton("Oui")
        self.ab_no = QRadioButton("Non")

        # Définir l'état initial
        if self.use_ab_testing:
            self.ab_yes.setChecked(True)
        else:
            self.ab_no.setChecked(True)

        # Groupement pour un choix exclusif
        self.ab_group = QButtonGroup()
        self.ab_group.addButton(self.ab_yes)
        self.ab_group.addButton(self.ab_no)

        # Connecter le signal
        self.ab_yes.toggled.connect(self.on_ab_toggle)

        self.message_b_label = QLabel("Message Template B (A/B):")
        self.message_b_label.setObjectName("messageConfig")
        self.message_b_button = QPushButton(self.get_message_preview(self.message_b_text))
        self.message_b_button.clicked.connect(self.edit_message_b)

        # Layout principal
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.message_a_label)
        self.layout.addWidget(self.message_a_button)

        # Ajout de la question et des boutons dans le layout principal
        self.layout.addWidget(self.ab_label)
        self.layout.addWidget(self.ab_yes)
        self.layout.addWidget(self.ab_no)

        self.layout.addWidget(self.message_b_label)
        self.layout.addWidget(self.message_b_button)

        # Afficher/masquer le champ B en fonction de l'état initial
        self.toggle_ab_testing(self.use_ab_testing)

    def get_message_preview(self, message):
        if message:
            return message[:50] + '...' if len(message) > 50 else message
        return "Message vide, cliquez pour remplir"

    def edit_message_a(self):
        dialog = MessageEditDialog("Éditer Message Template A", self.message_a_text)
        if dialog.exec():
            self.message_a_text = dialog.get_text()
            self.update_buttons_text()

    def edit_message_b(self):
        dialog = MessageEditDialog("Éditer Message Template B", self.message_b_text)
        if dialog.exec():
            self.message_b_text = dialog.get_text()
            self.update_buttons_text()

    def on_ab_toggle(self, checked):
        # Ce slot est appelé quand on clique sur Oui
        if self.ab_yes.isChecked():
            self.use_ab_testing = True
        else:
            self.use_ab_testing = False
        self.toggle_ab_testing(self.use_ab_testing)

    def toggle_ab_testing(self, state):
        # Montre ou cache le message B
        self.message_b_label.setVisible(state)
        self.message_b_button.setVisible(state)

    def validate(self):
        # A doit être rempli
        if not self.message_a_text:
            return False
        # Si A/B testing est utilisé, B doit être rempli
        if self.use_ab_testing and not self.message_b_text:
            return False
        return True

    def save_configuration(self):
        self.config_manager.update({
            'MESSAGE_A': self.message_a_text,
            'MESSAGE_B': self.message_b_text,
            'USE_AB_TESTING': self.use_ab_testing
        })

    def reload_configuration(self):
        # Recharge les valeurs depuis le config_manager
        self.message_a_text = self.config_manager.get('MESSAGE_A', '')
        self.message_b_text = self.config_manager.get('MESSAGE_B', '')
        self.use_ab_testing = self.config_manager.get('USE_AB_TESTING', False)
        self.ab_yes.setChecked(self.use_ab_testing)
        self.ab_no.setChecked(not self.use_ab_testing)
        self.update_buttons_text()
        self.toggle_ab_testing(self.use_ab_testing)

    def update_buttons_text(self):
        self.message_a_button.setText(self.get_message_preview(self.message_a_text))
        self.message_b_button.setText(self.get_message_preview(self.message_b_text))

# ultimate_main_window.py
from PySide6.QtCore import Qt
from controllers.main_controller import MainController
from services.chatgpt_manager import ChatGPTManager
from ui.premium_main_window import PremiumMainWindow
from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, QTextEdit, \
    QMessageBox, QLineEdit, QHBoxLayout, QSizePolicy, QRadioButton, QButtonGroup
import logging
from config.config import update_config

class UltimateMainWindow(PremiumMainWindow):
    def setup_ui(self):
        """Configure l'UI pour les utilisateurs Ultimate avec une seule colonne,
        avec un titre centré en haut et le bouton 'Start Bot' en bas."""

        # Créer le layout principal en vertical
        self.main_vertical_layout = QVBoxLayout()
        self.main_layout.addLayout(self.main_vertical_layout)

        # Créer le titre centré
        self.setup_title()
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_vertical_layout.addWidget(self.title_label)

        # Au lieu de 3 colonnes, on va tout mettre dans un seul layout vertical
        # Ajouter les éléments "généraux"
        self.setup_general_column()

        # Ajouter les éléments "messaging"
        self.setup_messaging_column()

        # Ajouter les éléments "ultimate" si disponible
        self.setup_ultimate_column()

        # Ajouter la case à cocher du mode test
        self.test_mode_checkbox = QCheckBox("Activer le mode test")
        self.test_mode_checkbox.setFont(self.font)
        self.main_vertical_layout.addWidget(self.test_mode_checkbox)
        test_mode_enabled = self.config.get('TEST_MODE_ENABLED', False)
        self.test_mode_checkbox.setChecked(test_mode_enabled)

        # Ajouter un espace vide pour pousser le bouton "Start Bot" en bas
        self.main_vertical_layout.addStretch()

        # Ajouter le bouton "Start Bot" centré
        self.setup_start_button()
        self.start_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.start_button_layout = QHBoxLayout()
        self.start_button_layout.addStretch()
        self.start_button_layout.addWidget(self.start_button)
        self.start_button_layout.addStretch()
        self.main_vertical_layout.addLayout(self.start_button_layout)

        # Ajuster la taille minimale de la fenêtre
        self.setMinimumWidth(1200)

    def setup_general_column(self):
        """Configure les éléments généraux et les ajoute directement à la disposition principale."""
        self.setup_linkedin_credentials()
        self.main_vertical_layout.addWidget(self.username_label)
        self.main_vertical_layout.addWidget(self.username_input)
        self.main_vertical_layout.addWidget(self.password_label)
        self.main_vertical_layout.addWidget(self.password_input)

        self.setup_search_link()
        self.main_vertical_layout.addWidget(self.search_link_label)
        self.main_vertical_layout.addWidget(self.search_link_input)

        self.setup_messages_per_day()
        self.main_vertical_layout.addWidget(self.messages_per_day_label)
        self.main_vertical_layout.addWidget(self.messages_per_day_input)

    def setup_messaging_column(self):
        """Configure les éléments de messagerie et les ajoute à la disposition principale."""
        self.setup_message_type_selection()
        # Choix du type de message
        self.main_vertical_layout.addWidget(self.message_type_label)
        self.main_vertical_layout.addWidget(self.normal_message_radio)
        self.main_vertical_layout.addWidget(self.chatgpt_message_radio)

        # Messages Template A/B
        self.setup_message_templates()
        self.main_vertical_layout.addWidget(self.message_a_label)
        self.main_vertical_layout.addWidget(self.message_a_button)
        self.main_vertical_layout.addWidget(self.message_b_label)
        self.main_vertical_layout.addWidget(self.message_b_button)

        # Clé API OpenAI et prompt personnalisé
        self.setup_premium_ui()
        self.main_vertical_layout.addWidget(self.api_key_label)
        self.main_vertical_layout.addWidget(self.api_key_input)
        self.main_vertical_layout.addWidget(self.prospecting_assistant_id_label)
        self.main_vertical_layout.addWidget(self.prospecting_assistant_id_input)

    def setup_ultimate_column(self):
        """Configure les éléments Ultimate (analyse de profil) et les ajoute à la disposition principale s'ils sont dispos."""
        if self.config.get('LICENSE_TYPE') == 'ultimate':
            # Activer les fonctionnalités Ultimate
            self.setup_ultimate_features()

            # Déplacer les composants Ultimate
            self.main_vertical_layout.addWidget(self.auto_reply_assistant_id_label)
            self.main_vertical_layout.addWidget(self.auto_reply_assistant_id_input)

            # Ajouter la section "Analyser les profils"
            self.main_vertical_layout.addWidget(self.analyze_profiles_checkbox)
            self.main_vertical_layout.addWidget(self.relevance_prompt_label)
            self.main_vertical_layout.addWidget(self.relevance_prompt_input)

            # Masquer ou afficher les champs en fonction de la case à cocher
            self.toggle_auto_reply_fields()
        # Si pas d'ultimate, rien n'est ajouté pour cette partie

    def setup_ultimate_features(self):
        """Ajoute les fonctionnalités spécifiques au plan Ultimate."""
        font = self.font

        # Label pour la question
        self.auto_reply_label = QLabel("Voulez-vous que l’IA réponde automatiquement aux messages privés ?")
        self.auto_reply_label.setFont(font)
        self.main_vertical_layout.addWidget(self.auto_reply_label)

        # Boutons radio pour Oui/Non
        self.auto_reply_yes_radio = QRadioButton("Oui")
        self.auto_reply_no_radio = QRadioButton("Non")

        self.auto_reply_yes_radio.setFont(font)
        self.auto_reply_no_radio.setFont(font)

        # Créer un groupe pour les boutons radio de réponse automatique
        self.auto_reply_group = QButtonGroup(self)
        self.auto_reply_group.addButton(self.auto_reply_yes_radio)
        self.auto_reply_group.addButton(self.auto_reply_no_radio)

        # Mise en page verticale pour les boutons radio
        self.auto_reply_radio_layout = QVBoxLayout()
        self.auto_reply_radio_layout.addWidget(self.auto_reply_yes_radio)
        self.auto_reply_radio_layout.addWidget(self.auto_reply_no_radio)
        self.main_vertical_layout.addLayout(self.auto_reply_radio_layout)

        # Charger l'état depuis la configuration
        auto_reply_enabled = self.config.get('AUTO_REPLY_ENABLED', False)
        if auto_reply_enabled:
            self.auto_reply_yes_radio.setChecked(True)
        else:
            self.auto_reply_no_radio.setChecked(True)

        # Champs pour l'assistant_id des réponses automatiques
        self.auto_reply_assistant_id_label = QLabel("Assistant ID pour les réponses automatiques:")
        self.auto_reply_assistant_id_label.setFont(font)
        self.auto_reply_assistant_id_input = QLineEdit(self.config.get('AUTO_REPLY_ASSISTANT_ID', ''))
        self.auto_reply_assistant_id_input.setFont(font)
        self.main_vertical_layout.addWidget(self.auto_reply_assistant_id_label)
        self.main_vertical_layout.addWidget(self.auto_reply_assistant_id_input)

        # Cacher les champs de réponse auto si non activés
        self.toggle_auto_reply_fields()

        # Connecter les boutons radio au toggle
        self.auto_reply_yes_radio.toggled.connect(self.toggle_auto_reply_fields)

    def toggle_auto_reply_fields(self):
        """Afficher ou masquer les champs de réponse automatique en fonction du bouton Oui."""
        # Si Oui est sélectionné => auto_reply_enabled = True
        if self.auto_reply_yes_radio.isChecked():
            self.auto_reply_assistant_id_label.show()
            self.auto_reply_assistant_id_input.show()
        else:
            self.auto_reply_assistant_id_label.hide()
            self.auto_reply_assistant_id_input.hide()

    def validate_inputs(self):
        """Valide les entrées de l'utilisateur avec la nouvelle logique de réponses automatiques."""
        username = self.username_input.text()
        password = self.password_input.text()
        search_link = self.search_link_input.text()
        messages_per_day = self.messages_per_day_input.text()

        if not all([username, password, search_link, messages_per_day]):
            QMessageBox.warning(self, "Erreur de saisie", "Tous les champs doivent être remplis !")
            logging.error("Erreur de saisie : Tous les champs doivent être remplis !")
            return False

        try:
            self.messages_per_day_int = int(messages_per_day)
            if not (0 <= self.messages_per_day_int <= 30):
                QMessageBox.warning(
                    self, "Erreur de saisie",
                    "Le nombre de messages par jour doit être entre 0 et 30 pour le plan Ultimate !"
                )
                logging.error(
                    "Erreur de saisie : Le nombre de messages par jour doit être entre 0 et 30 pour le plan Ultimate !")
                return False
        except ValueError:
            QMessageBox.warning(
                self, "Erreur de saisie",
                "Le nombre de messages par jour doit être un nombre valide !"
            )
            logging.error("Erreur de saisie : Le nombre de messages par jour doit être un nombre valide !")
            return False

        # Validation des messages Template A et B si message normal
        if self.normal_message_radio.isChecked():
            if not self.message_a_text or not self.message_b_text:
                QMessageBox.warning(self, "Erreur de saisie", "Les messages Template A et B doivent être remplis !")
                logging.error("Erreur de saisie : Les messages Template A et B doivent être remplis !")
                return False
        elif self.chatgpt_message_radio.isChecked():
            api_key = self.api_key_input.text()
            prospecting_assistant_id = self.prospecting_assistant_id_input.text()
            if not api_key or not prospecting_assistant_id:
                QMessageBox.warning(self, "Erreur de saisie",
                                    "Veuillez remplir la clé API et le prompt pour ChatGPT.")
                logging.error(
                    "Erreur de saisie : Les champs Clé API et Assistant ID de prospection doivent être remplis.")
                return False

        # Vérifier le champ Assistant ID pour les réponses auto si Oui
        if self.auto_reply_yes_radio.isChecked():
            auto_reply_assistant_id = self.auto_reply_assistant_id_input.text()
            if not auto_reply_assistant_id:
                QMessageBox.warning(self, "Erreur de saisie",
                                    "Veuillez entrer l'Assistant ID pour les réponses automatiques.")
                logging.error("Erreur de saisie : L'Assistant ID doit être rempli.")
                return False

        return True

    def save_configuration(self):
        """Sauvegarde la configuration mise à jour, y compris les paramètres Ultimate et le mode test."""
        # Appeler la méthode de sauvegarde de la classe parent pour enregistrer la config de base
        super().save_configuration()

        # Déterminer si auto_reply est activé
        auto_reply_enabled = self.auto_reply_yes_radio.isChecked()
        test_mode_enabled = self.test_mode_checkbox.isChecked()

        # Si auto_reply est activé, on met à jour l'assistant_id avec la valeur entrée par l'utilisateur
        if auto_reply_enabled:
            self.config['AUTO_REPLY_ASSISTANT_ID'] = self.auto_reply_assistant_id_input.text()

        # Mettre à jour l'état de l'auto_reply et du mode test
        self.config['AUTO_REPLY_ENABLED'] = auto_reply_enabled
        self.config['TEST_MODE_ENABLED'] = test_mode_enabled

        update_config(self.config)
        logging.debug("Configuration Ultimate mise à jour avec succès")

    def start_bot(self):
        """Démarre le bot en utilisant les fonctionnalités spécifiques au plan Ultimate."""
        logging.debug("Start Bot button clicked (Ultimate)")

        # Valider les entrées premium pour le plan Ultimate
        if self.chatgpt_message_radio.isChecked():
            if not self.validate_premium_inputs():
                return
            # Sauvegarder la configuration premium
            self.save_premium_configuration()
        else:
            # Sauvegarder la configuration pour le type normal
            self.save_premium_configuration()

        # Valider les entrées de base
        if not self.validate_inputs():
            return

        # Sauvegarder la configuration de base
        self.save_configuration()

        # Exécuter le bot
        self.run_ultimate_bot()

    def run_ultimate_bot(self):
        """Exécute le bot avec les fonctionnalités spécifiques au plan Ultimate."""
        openai_api_key = self.api_key_input.text()
        auto_reply_enabled = self.auto_reply_yes_radio.isChecked()
        auto_reply_assistant_id = self.auto_reply_assistant_id_input.text() if auto_reply_enabled else ''

        analyze_profiles = False
        relevance_prompt = None
        if hasattr(self, 'analyze_profiles_checkbox') and self.analyze_profiles_checkbox.isChecked():
            analyze_profiles = True
            relevance_prompt = self.relevance_prompt_input.toPlainText()

        test_mode_enabled = self.test_mode_checkbox.isChecked()

        self.chatgpt_manager = ChatGPTManager(
            api_key=openai_api_key,
            relevance_prompt_template=relevance_prompt
        )

        self.controller = MainController(
            username=self.username_input.text(),
            password=self.password_input.text(),
            search_link=self.search_link_input.text(),
            messages_per_day=self.messages_per_day_int,
            message_a=self.message_a_text,
            message_b=self.message_b_text,
            chatgpt_manager=self.chatgpt_manager,
            message_type='chatgpt' if self.chatgpt_message_radio.isChecked() else 'normal',
            analyze_profiles=analyze_profiles,
            auto_reply_enabled=auto_reply_enabled,
            auto_reply_assistant_id=auto_reply_assistant_id,
            prospecting_assistant_id=self.prospecting_assistant_id_input.text(),
            test_mode_enabled=test_mode_enabled
        )

        limit_reached, messages_sent = self.controller.data_manager.has_reached_message_limit(self.messages_per_day_int)

        if limit_reached and not auto_reply_enabled:
            QMessageBox.warning(
                self, "Limite atteinte",
                f"Le bot a déjà envoyé le nombre maximum de messages aujourd'hui ({messages_sent}/{self.messages_per_day_int})."
            )
            logging.info("Limite quotidienne de messages atteinte, le bot ne démarrera pas.")
            return

        try:
            logging.debug("Bot démarré avec succès (Ultimate)")
            self.controller.run()
            logging.debug("Méthode run() de MainController appelée")

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

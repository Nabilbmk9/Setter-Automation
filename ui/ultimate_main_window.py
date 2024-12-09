# ultimate_main_window.py
from PySide6.QtCore import Qt
from controllers.main_controller import MainController
from services.chatgpt_manager import ChatGPTManager
from ui.premium_main_window import PremiumMainWindow
from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, QTextEdit, \
    QMessageBox, QLineEdit, QHBoxLayout, QSizePolicy
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
            self.main_vertical_layout.addWidget(self.auto_reply_checkbox)
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

        # Case à cocher pour activer la réponse automatique
        self.auto_reply_checkbox = QCheckBox("Activer la réponse automatique")
        self.auto_reply_checkbox.setFont(font)
        self.auto_reply_checkbox.stateChanged.connect(self.toggle_auto_reply_fields)
        self.main_layout.addWidget(self.auto_reply_checkbox)

        # Champ pour l'assistant_id des réponses automatiques
        self.auto_reply_assistant_id_label = QLabel("Assistant ID pour les réponses automatiques:")
        self.auto_reply_assistant_id_label.setFont(font)
        self.auto_reply_assistant_id_input = QLineEdit(self.config.get('AUTO_REPLY_ASSISTANT_ID', ''))
        self.auto_reply_assistant_id_input.setFont(font)

        # Masquer les champs de réponse automatique par défaut
        self.auto_reply_assistant_id_label.hide()
        self.auto_reply_assistant_id_input.hide()

        # Charger l'état de la case à cocher depuis la configuration
        auto_reply_enabled = self.config.get('AUTO_REPLY_ENABLED', False)
        self.auto_reply_checkbox.setChecked(auto_reply_enabled)

    def toggle_auto_reply_fields(self):
        """Afficher ou masquer les champs de réponse automatique."""
        if self.auto_reply_checkbox.isChecked():
            self.auto_reply_assistant_id_label.show()
            self.auto_reply_assistant_id_input.show()
        else:
            self.auto_reply_assistant_id_label.hide()
            self.auto_reply_assistant_id_input.hide()

    def validate_inputs(self):
        """Valide les entrées de l'utilisateur en tenant compte du plan Ultimate, avec messages_per_day entre 0 et 30."""
        username = self.username_input.text()
        password = self.password_input.text()
        search_link = self.search_link_input.text()
        messages_per_day = self.messages_per_day_input.text()

        # Vérifier que les champs de base sont remplis
        if not all([username, password, search_link, messages_per_day]):
            QMessageBox.warning(self, "Erreur de saisie", "Tous les champs doivent être remplis !")
            logging.error("Erreur de saisie : Tous les champs doivent être remplis !")
            return False

        # Valider `messages_per_day` pour être entre 0 et 30
        try:
            self.messages_per_day_int = int(messages_per_day)
            if not (0 <= self.messages_per_day_int <= 30):
                QMessageBox.warning(
                    self, "Erreur de saisie",
                    "Le nombre de messages par jour doit être entre 0 et 30 pour le plan Ultimate !"
                )
                logging.error(
                    "Erreur de saisie : Le nombre de messages par jour doit être entre 0 et 30 pour le plan Ultimate !"
                )
                return False
        except ValueError:
            QMessageBox.warning(
                self, "Erreur de saisie",
                "Le nombre de messages par jour doit être un nombre valide !"
            )
            logging.error("Erreur de saisie : Le nombre de messages par jour doit être un nombre valide !")
            return False

        # Validation supplémentaire
        if self.normal_message_radio.isChecked():
            # Vérifier que les messages Template A et B ne sont pas vides
            if not self.message_a_text or not self.message_b_text:
                QMessageBox.warning(self, "Erreur de saisie", "Les messages Template A et B doivent être remplis !")
                logging.error("Erreur de saisie : Les messages Template A et B doivent être remplis !")
                return False

        elif self.chatgpt_message_radio.isChecked():
            # Vérifier que l’API Key et l'assistant id de prospection sont remplis
            api_key = self.api_key_input.text()
            prospecting_assistant_id = self.prospecting_assistant_id_input.text()

            if not api_key or not prospecting_assistant_id:
                QMessageBox.warning(self, "Erreur de saisie",
                                    "Veuillez remplir la clé API et le prompt pour ChatGPT.")
                logging.error("Erreur de saisie : Les champs Clé API et Assistant ID de prospection doivent être remplis.")
                return False

        # Vérifier les champs spécifiques pour les réponses automatiques
        if hasattr(self, 'auto_reply_checkbox') and self.auto_reply_checkbox.isChecked():
            auto_reply_assistant_id = self.auto_reply_assistant_id_input.text()
            if not auto_reply_assistant_id:
                QMessageBox.warning(self, "Erreur de saisie",
                                    "Veuillez entrer l'Assistant ID pour les réponses automatiques.")
                logging.error("Erreur de saisie : L'Assistant ID doit être rempli.")
                return False

        return True

    def save_configuration(self):
        """Sauvegarde la configuration mise à jour, y compris les paramètres Ultimate et le mode test."""
        # Appeler la méthode de sauvegarde de la classe parent
        super().save_configuration()

        # Enregistrer les paramètres Ultimate
        auto_reply_enabled = False
        auto_reply_assistant_id = ''

        if hasattr(self, 'auto_reply_checkbox'):
            auto_reply_enabled = self.auto_reply_checkbox.isChecked()
        if hasattr(self, 'auto_reply_assistant_id_input'):
            auto_reply_assistant_id = self.auto_reply_assistant_id_input.text()

        # Enregistrer l'état du mode test
        test_mode_enabled = self.test_mode_checkbox.isChecked()

        self.config.update({
            'AUTO_REPLY_ENABLED': auto_reply_enabled,
            'AUTO_REPLY_ASSISTANT_ID': auto_reply_assistant_id,
            'TEST_MODE_ENABLED': test_mode_enabled,
        })
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
        # Utiliser ChatGPT pour générer les messages
        openai_api_key = self.api_key_input.text()
        auto_reply_assistant_id = ''
        if hasattr(self, 'auto_reply_assistant_id_input'):
            auto_reply_assistant_id = self.auto_reply_assistant_id_input.text()

        analyze_profiles = False
        relevance_prompt = None
        if hasattr(self, 'analyze_profiles_checkbox') and self.analyze_profiles_checkbox.isChecked():
            analyze_profiles = True
            relevance_prompt = self.relevance_prompt_input.toPlainText()

        # Récupérer l'état du mode test à partir de la case à cocher
        test_mode_enabled = self.test_mode_checkbox.isChecked()

        # Créer une instance de ChatGPTManager avec les paramètres appropriés
        self.chatgpt_manager = ChatGPTManager(
            api_key=openai_api_key,
            relevance_prompt_template=relevance_prompt
        )

        # Créer le contrôleur avec l’assistant_id et l’option auto_reply_enabled
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
            auto_reply_enabled=(hasattr(self, 'auto_reply_checkbox') and self.auto_reply_checkbox.isChecked()),
            auto_reply_assistant_id=auto_reply_assistant_id,
            prospecting_assistant_id=self.prospecting_assistant_id_input.text(),
            test_mode_enabled=test_mode_enabled
        )

        # Vérifier si la limite quotidienne de messages est atteinte
        limit_reached, messages_sent = self.controller.data_manager.has_reached_message_limit(self.messages_per_day_int)

        # Si la limite est atteinte mais auto_reply est activé, ne pas bloquer l’exécution
        if limit_reached and not (hasattr(self, 'auto_reply_checkbox') and self.auto_reply_checkbox.isChecked()):
            QMessageBox.warning(
                self, "Limite atteinte",
                f"Le bot a déjà envoyé le nombre maximum de messages aujourd'hui ({messages_sent}/{self.messages_per_day_int})."
            )
            logging.info("Limite quotidienne de messages atteinte, le bot ne démarrera pas.")
            return

        # Démarrer le bot
        try:
            logging.debug("Bot démarré avec succès (Ultimate)")
            self.controller.run()
            logging.debug("Méthode run() de MainController appelée")

            # Si auto_reply est activé, informer que le bot reste actif pour gérer les réponses
            if hasattr(self, 'auto_reply_checkbox') and self.auto_reply_checkbox.isChecked():
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

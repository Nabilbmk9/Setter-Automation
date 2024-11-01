# ultimate_main_window.py
from PySide6.QtCore import Qt

from controllers.main_controller import MainController
from services.chatgpt_manager import ChatGPTManager
from ui.premium_main_window import PremiumMainWindow
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QCheckBox, QLabel, QTextEdit, \
    QMessageBox, QLineEdit
import logging
from config.config import update_config


class UltimateMainWindow(PremiumMainWindow):
    def setup_ui(self):
        """Configure l'UI pour les utilisateurs Ultimate avec une disposition en colonnes, avec un titre centré en haut et le bouton 'Start Bot' en bas."""
        # Créer le layout principal en vertical
        self.main_vertical_layout = QVBoxLayout()
        self.main_layout.addLayout(self.main_vertical_layout)

        # Créer le titre centré
        self.setup_title()
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_vertical_layout.addWidget(self.title_label)

        # Créer le layout principal en horizontal pour les colonnes
        self.columns_layout = QHBoxLayout()
        self.main_vertical_layout.addLayout(self.columns_layout)

        # Colonne 1 : Paramètres généraux
        self.general_column = QWidget()
        self.general_layout = QVBoxLayout()
        self.general_column.setLayout(self.general_layout)

        # Colonne 2 : Paramètres de messagerie
        self.messaging_column = QWidget()
        self.messaging_layout = QVBoxLayout()
        self.messaging_column.setLayout(self.messaging_layout)

        # Colonne 3 : Fonctionnalités Ultimate (y compris analyse de profil)
        self.ultimate_column = QWidget()
        self.ultimate_layout = QVBoxLayout()
        self.ultimate_column.setLayout(self.ultimate_layout)

        # Ajouter les colonnes au layout principal
        self.columns_layout.addWidget(self.general_column)
        self.columns_layout.addWidget(self.messaging_column)
        self.columns_layout.addWidget(self.ultimate_column)

        # Appeler les méthodes pour configurer les composants, en les ajoutant aux colonnes appropriées
        self.setup_general_column()
        self.setup_messaging_column()
        self.setup_ultimate_column()

        # Ajouter un espace vide pour pousser le bouton en bas
        self.main_vertical_layout.addStretch()

        # Ajouter le bouton "Start Bot" centré
        self.setup_start_button()
        self.start_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.start_button_layout = QHBoxLayout()
        self.start_button_layout.addStretch()
        self.start_button_layout.addWidget(self.start_button)
        self.start_button_layout.addStretch()

        # Ajouter le layout du bouton au layout principal vertical
        self.main_vertical_layout.addLayout(self.start_button_layout)

        # Ajuster la taille minimale de la fenêtre pour s'adapter aux colonnes
        self.setMinimumWidth(1200)

    def setup_general_column(self):
        """Configure les éléments de la colonne des paramètres généraux."""
        # Déplacer les composants dans le layout de la colonne générale
        self.setup_linkedin_credentials()
        self.general_layout.addWidget(self.username_label)
        self.general_layout.addWidget(self.username_input)
        self.general_layout.addWidget(self.password_label)
        self.general_layout.addWidget(self.password_input)

        self.setup_search_link()
        self.general_layout.addWidget(self.search_link_label)
        self.general_layout.addWidget(self.search_link_input)

        self.setup_messages_per_day()
        self.general_layout.addWidget(self.messages_per_day_label)
        self.general_layout.addWidget(self.messages_per_day_input)

        # Ajouter un espace vide pour pousser le contenu vers le haut
        self.general_layout.addStretch()

    def setup_messaging_column(self):
        """Configure les éléments de la colonne des paramètres de messagerie."""
        self.setup_message_type_selection()
        # Choix du type de message
        self.messaging_layout.addWidget(self.message_type_label)
        self.messaging_layout.addWidget(self.normal_message_radio)
        self.messaging_layout.addWidget(self.chatgpt_message_radio)

        # Messages Template A/B
        self.setup_message_templates()
        self.messaging_layout.addWidget(self.message_a_label)
        self.messaging_layout.addWidget(self.message_a_button)
        self.messaging_layout.addWidget(self.message_b_label)
        self.messaging_layout.addWidget(self.message_b_button)

        # Clé API OpenAI et prompt personnalisé
        self.setup_premium_ui()
        self.messaging_layout.addWidget(self.api_key_label)
        self.messaging_layout.addWidget(self.api_key_input)
        self.messaging_layout.addWidget(self.prompt_label)
        self.messaging_layout.addWidget(self.prompt_input)

    def setup_ultimate_column(self):
        """Configure les éléments de la colonne des fonctionnalités Ultimate (y compris analyse de profil)."""
        # Vérifier si l'utilisateur a une licence 'ultimate'
        if self.config.get('LICENSE_TYPE') == 'ultimate':
            # Activer les fonctionnalités Ultimate
            self.setup_ultimate_features()

            # Déplacer les composants Ultimate dans le layout de la colonne Ultimate
            self.ultimate_layout.addWidget(self.auto_reply_checkbox)
            self.ultimate_layout.addWidget(self.assistant_id_label)
            self.ultimate_layout.addWidget(self.assistant_id_input)

            # Ajouter la section "Analyser les profils"
            self.ultimate_layout.addWidget(self.analyze_profiles_checkbox)
            self.ultimate_layout.addWidget(self.relevance_prompt_label)
            self.ultimate_layout.addWidget(self.relevance_prompt_input)

            # Masquer ou afficher les champs en fonction de la case à cocher
            self.toggle_auto_reply_fields()
        else:
            # Si l'utilisateur n'a pas la licence 'ultimate', masquer la colonne
            self.ultimate_column.hide()

    def setup_ultimate_features(self):
        """Ajoute les fonctionnalités spécifiques au plan Ultimate."""
        font = self.font

        # Case à cocher pour activer la réponse automatique
        self.auto_reply_checkbox = QCheckBox("Activer la réponse automatique")
        self.auto_reply_checkbox.setFont(font)
        self.auto_reply_checkbox.stateChanged.connect(self.toggle_auto_reply_fields)
        self.main_layout.addWidget(self.auto_reply_checkbox)

        # Champ pour l'assistant_id
        self.assistant_id_label = QLabel("Assistant ID pour les réponses automatiques:")
        self.assistant_id_label.setFont(font)
        self.assistant_id_input = QLineEdit(self.config.get('ASSISTANT_ID', ''))
        self.assistant_id_input.setFont(font)
        self.ultimate_layout.addWidget(self.assistant_id_label)
        self.ultimate_layout.addWidget(self.assistant_id_input)

        # Masquer les champs de réponse automatique par défaut
        self.assistant_id_label.hide()
        self.assistant_id_input.hide()

        # Charger l'état de la case à cocher depuis la configuration
        auto_reply_enabled = self.config.get('AUTO_REPLY_ENABLED', False)
        self.auto_reply_checkbox.setChecked(auto_reply_enabled)

    def toggle_auto_reply_fields(self):
        """Afficher ou masquer les champs de réponse automatique."""
        if self.auto_reply_checkbox.isChecked():
            self.assistant_id_label.show()
            self.assistant_id_input.show()
        else:
            self.assistant_id_label.hide()
            self.assistant_id_input.hide()

    def validate_inputs(self):
        """Valide les entrées de l'utilisateur en tenant compte du plan Ultimate, avec messages_per_day entre 0 et 30."""

        # Vérification des champs de base (email, mot de passe, lien de recherche)
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

        # Validation supplémentaire en fonction du type de message
        if self.normal_message_radio.isChecked():
            # Vérifier que les messages Template A et B ne sont pas vides
            if not self.message_a_text or not self.message_b_text:
                QMessageBox.warning(self, "Erreur de saisie", "Les messages Template A et B doivent être remplis !")
                logging.error("Erreur de saisie : Les messages Template A et B doivent être remplis !")
                return False

        elif self.chatgpt_message_radio.isChecked():
            # Vérifier que l’API Key et le prompt sont remplis
            api_key = self.api_key_input.text()
            custom_prompt = self.prompt_input.toPlainText()

            if not api_key or not custom_prompt:
                QMessageBox.warning(self, "Erreur de saisie",
                                    "Veuillez remplir la clé API et le prompt pour ChatGPT.")
                logging.error("Erreur de saisie : Les champs Clé API et Prompt doivent être remplis pour ChatGPT.")
                return False

        # Vérifier les champs spécifiques pour les réponses automatiques si elles sont activées
        if self.auto_reply_checkbox.isChecked():
            assistant_id = self.assistant_id_input.text()
            if not assistant_id:
                QMessageBox.warning(self, "Erreur de saisie",
                                    "Veuillez entrer l'Assistant ID pour les réponses automatiques.")
                logging.error("Erreur de saisie : L'Assistant ID doit être rempli.")
                return False

        return True

    def save_configuration(self):
        """Sauvegarde la configuration mise à jour, y compris les paramètres Ultimate."""
        # Appeler la méthode de sauvegarde de la classe parent
        super().save_configuration()

        # Enregistrer les paramètres Ultimate
        auto_reply_enabled = self.auto_reply_checkbox.isChecked()
        assistant_id = self.assistant_id_input.text()

        self.config.update({
            'AUTO_REPLY_ENABLED': auto_reply_enabled,
            'ASSISTANT_ID': assistant_id,
        })
        update_config(self.config)
        logging.debug("Configuration Ultimate mise à jour avec succès")

    def run_bot(self):
        """Exécute le bot avec les fonctionnalités Ultimate."""
        # Vous pouvez surcharger cette méthode pour inclure les fonctionnalités Ultimate
        # ou appeler la méthode de la classe parent si elle convient
        self.run_ultimate_bot()

    def run_ultimate_bot(self):
        """Exécute le bot avec les fonctionnalités spécifiques au plan Ultimate."""
        # Utiliser ChatGPT pour générer les messages
        openai_api_key = self.api_key_input.text()
        assistant_id = self.assistant_id_input.text()
        custom_prompt = self.prompt_input.toPlainText()

        # Vérifier si l'analyse de profil est activée
        analyze_profiles = self.analyze_profiles_checkbox.isChecked()
        relevance_prompt = self.relevance_prompt_input.toPlainText() if analyze_profiles else None

        # Créer une instance de ChatGPTManager avec les paramètres appropriés
        self.chatgpt_manager = ChatGPTManager(
            api_key=openai_api_key,
            prompt_template=custom_prompt,
            relevance_prompt_template=relevance_prompt
        )

        # Créer le contrôleur avec l'assistant_id et l'option auto_reply_enabled
        self.controller = MainController(
            username=self.username_input.text(),
            password=self.password_input.text(),
            search_link=self.search_link_input.text(),
            messages_per_day=self.messages_per_day_int,
            chatgpt_manager=self.chatgpt_manager,
            message_type='chatgpt' if self.chatgpt_message_radio.isChecked() else 'normal',
            analyze_profiles=analyze_profiles,
            auto_reply_enabled=self.auto_reply_checkbox.isChecked(),
            assistant_id=assistant_id
        )

        # Vérifier si la limite quotidienne de messages est atteinte
        limit_reached, messages_sent = self.controller.data_manager.has_reached_message_limit(self.messages_per_day_int)
        if limit_reached:
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

            if self.auto_reply_checkbox.isChecked():
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

# premium_features_mixin.py

from PySide6.QtWidgets import QLabel, QLineEdit, QTextEdit, QMessageBox, QRadioButton, QCheckBox, QButtonGroup
from PySide6.QtGui import QFont
from config.config import update_config
import logging

from controllers.main_controller import MainController
from services.chatgpt_manager import ChatGPTManager
from openai import OpenAIError


class PremiumFeaturesMixin:
    def setup_message_type_selection(self):
        """Configure les boutons radio pour le choix du type de message."""
        font = self.font

        # Choix du type de message
        self.message_type_label = QLabel("Type de message à envoyer:")
        self.message_type_label.setFont(font)
        self.main_layout.addWidget(self.message_type_label)

        # Créer un groupe pour les boutons radio du choix de message
        self.message_type_group = QButtonGroup(self)
        # Boutons radio pour le choix
        self.normal_message_radio = QRadioButton("Messages normaux (Templates A/B)")
        self.normal_message_radio.setFont(font)
        self.normal_message_radio.setChecked(True)  # Par défaut
        self.message_type_group.addButton(self.normal_message_radio)  # Ajouter au groupe
        self.main_layout.addWidget(self.normal_message_radio)

        self.chatgpt_message_radio = QRadioButton("Messages personnalisés avec ChatGPT")
        self.chatgpt_message_radio.setFont(font)
        self.message_type_group.addButton(self.chatgpt_message_radio)  # Ajouter au groupe
        self.main_layout.addWidget(self.chatgpt_message_radio)

        # Lire le type de message dans la configuration et ajuster le bouton sélectionné
        message_type = self.config.get('MESSAGE_TYPE', 'normal')  # 'normal' par défaut
        analyse_profil = self.config.get('ANALYZE_PROFILES', 'false')
        if message_type == 'normal':
            self.normal_message_radio.setChecked(True)
        else:
            self.chatgpt_message_radio.setChecked(True)



        # Connecter les signaux pour afficher/masquer les champs correspondants
        self.normal_message_radio.toggled.connect(self.toggle_message_fields)
        self.chatgpt_message_radio.toggled.connect(self.toggle_message_fields)

    def setup_premium_ui(self):
        """Configure les éléments de l'interface spécifiques aux fonctionnalités premium."""
        font = self.font

        # Clé API pour OpenAI
        self.api_key_label = QLabel("Clé API OpenAI:")
        self.api_key_label.setFont(font)
        self.api_key_input = QLineEdit(self.config.get('OPENAI_API_KEY', ''))
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setFont(font)
        self.main_layout.addWidget(self.api_key_label)
        self.main_layout.addWidget(self.api_key_input)

        # Assistant ID pour la prospection
        self.prospecting_assistant_id_label = QLabel("Assistant ID pour la prospection:")
        self.prospecting_assistant_id_label.setFont(font)
        self.prospecting_assistant_id_input = QLineEdit(self.config.get('PROSPECTING_ASSISTANT_ID', ''))
        self.prospecting_assistant_id_input.setFont(font)
        self.main_layout.addWidget(self.prospecting_assistant_id_label)
        self.main_layout.addWidget(self.prospecting_assistant_id_input)

        # Option pour activer/désactiver l'analyse de profil
        self.analyze_profiles_checkbox = QCheckBox("Analyser les profils avant d'envoyer les messages")
        self.analyze_profiles_checkbox.setFont(font)
        self.analyze_profiles_checkbox.stateChanged.connect(self.toggle_relevance_prompt)
        self.main_layout.addWidget(self.analyze_profiles_checkbox)

        # Lire la configuration pour activer ou désactiver la case à cocher
        analyze_profiles = self.config.get('ANALYZE_PROFILES', False)
        if analyze_profiles:
            self.analyze_profiles_checkbox.setChecked(True)

        # Prompt pour l'analyse des profils (caché par défaut)
        self.relevance_prompt_label = QLabel("Prompt pour l'analyse des profils:")
        self.relevance_prompt_label.setFont(font)
        self.relevance_prompt_input = QTextEdit(self.config.get('RELEVANCE_PROMPT', ''))
        self.relevance_prompt_input.setFont(font)
        self.main_layout.addWidget(self.relevance_prompt_label)
        self.main_layout.addWidget(self.relevance_prompt_input)

        # Masquer le prompt d'analyse de profil par défaut
        self.relevance_prompt_label.hide()
        self.relevance_prompt_input.hide()

        # Au démarrage, afficher/masquer les champs en fonction du bouton sélectionné
        self.toggle_message_fields()

    def toggle_message_fields(self):
        """Afficher ou masquer les champs en fonction du choix de l'utilisateur."""
        if self.normal_message_radio.isChecked():
            # Afficher les messages Template A et B
            self.message_a_label.show()
            self.message_a_button.show()
            self.message_b_label.show()
            self.message_b_button.show()

            # Masquer les champs ChatGPT
            self.api_key_label.hide()
            self.api_key_input.hide()
            self.prospecting_assistant_id_label.hide()
            self.prospecting_assistant_id_input.hide()
            self.analyze_profiles_checkbox.hide()
            self.relevance_prompt_label.hide()
            self.relevance_prompt_input.hide()
        else:
            # Masquer les messages Template A et B
            self.message_a_label.hide()
            self.message_a_button.hide()
            self.message_b_label.hide()
            self.message_b_button.hide()

            # Afficher les champs ChatGPT
            self.api_key_label.show()
            self.api_key_input.show()
            self.prospecting_assistant_id_label.show()
            self.prospecting_assistant_id_input.show()
            self.analyze_profiles_checkbox.show()

            # Vérifier l'état de la case à cocher pour l'analyse de profil
            if self.analyze_profiles_checkbox.isChecked():
                self.relevance_prompt_label.show()
                self.relevance_prompt_input.show()
            else:
                self.relevance_prompt_label.hide()
                self.relevance_prompt_input.hide()

    def toggle_relevance_prompt(self):
        """Afficher ou masquer le prompt d'analyse de profil en fonction de la case à cocher."""
        # Vérifier si les attributs sont initialisés avant de les utiliser
        if hasattr(self, 'relevance_prompt_label') and hasattr(self, 'relevance_prompt_input'):
            if self.analyze_profiles_checkbox.isChecked():
                self.relevance_prompt_label.show()
                self.relevance_prompt_input.show()
            else:
                self.relevance_prompt_label.hide()
                self.relevance_prompt_input.hide()
        else:
            logging.error(
                "Les composants relevance_prompt_label ou relevance_prompt_input ne sont pas encore initialisés.")

    def validate_premium_inputs(self):
        """Valide les entrées spécifiques aux fonctionnalités premium."""
        if self.chatgpt_message_radio.isChecked():
            api_key = self.api_key_input.text()
            prospecting_assistant_id = self.prospecting_assistant_id_input.text()

            if not api_key or not prospecting_assistant_id:
                QMessageBox.warning(self, "Erreur de saisie", "Veuillez remplir tous les champs pour ChatGPT.")
                logging.error("Erreur de saisie : Les champs Clé API et Prospection Assistant ID doivent être remplis pour ChatGPT.")
                return False

            # Si l'analyse de profil est activée, vérifier que le prompt d'analyse est fourni
            if self.analyze_profiles_checkbox.isChecked():
                relevance_prompt = self.relevance_prompt_input.toPlainText()
                if not relevance_prompt:
                    QMessageBox.warning(self, "Erreur de saisie", "Veuillez remplir le prompt pour l'analyse des profils.")
                    logging.error("Erreur de saisie : Le prompt d'analyse des profils doit être rempli.")
                    return False

            # Validation de la clé API avec OpenAI
            if not ChatGPTManager.validate_api_key(api_key):
                QMessageBox.critical(self, "Clé API invalide", "La clé API fournie est invalide. Veuillez vérifier.")
                logging.error("Validation échouée : Clé API invalide.")
                return False

        return True

    def save_premium_configuration(self):
        """Sauvegarde la configuration spécifique aux fonctionnalités premium."""
        # Déterminer le type de message choisi
        if self.normal_message_radio.isChecked():
            message_type = 'normal'
        else:
            message_type = 'chatgpt'

        # Enregistrer si l'analyse de profil est activée
        analyze_profiles = self.analyze_profiles_checkbox.isChecked()

        self.config.update({
            'MESSAGE_TYPE': message_type,
            'OPENAI_API_KEY': self.api_key_input.text(),
            'PROSPECTING_ASSISTANT_ID': self.prospecting_assistant_id_input.text(),
            'ANALYZE_PROFILES': analyze_profiles,
            'RELEVANCE_PROMPT': self.relevance_prompt_input.toPlainText()
        })
        update_config(self.config)
        logging.debug("Configuration premium mise à jour avec succès")

    def run_premium_bot(self):
        """Exécute le bot avec les fonctionnalités premium."""
        if self.chatgpt_message_radio.isChecked():
            # Utiliser ChatGPT pour générer les messages
            openai_api_key = self.api_key_input.text()
            prospecting_assistant_id = self.prospecting_assistant_id_input.toPlainText()

            # Vérifier si l'analyse de profil est activée
            analyze_profiles = self.analyze_profiles_checkbox.isChecked()
            relevance_prompt = self.relevance_prompt_input.toPlainText() if analyze_profiles else None

            # Créer une instance de ChatGPTManager avec les paramètres appropriés
            self.chatgpt_manager = ChatGPTManager(
                api_key=openai_api_key,
                prospecting_assistant_id=prospecting_assistant_id,
                relevance_prompt_template=relevance_prompt
            )

            # Créer le contrôleur avec le chatgpt_manager et l'option analyze_profiles
            self.controller = MainController(
                username=self.username_input.text(),
                password=self.password_input.text(),
                search_link=self.search_link_input.text(),
                messages_per_day=self.messages_per_day_int,
                chatgpt_manager=self.chatgpt_manager,
                message_type='chatgpt',
                analyze_profiles=analyze_profiles,  # Passer l'option au contrôleur
                prospecting_assistant_id=self.prospecting_assistant_id_input.text()
            )
        else:
            # Créer le contrôleur avec les messages Template A et B
            self.controller = MainController(
                username=self.username_input.text(),
                password=self.password_input.text(),
                search_link=self.search_link_input.text(),
                message_a=self.message_a_text,
                message_b=self.message_b_text,
                messages_per_day=self.messages_per_day_int,
                message_type='normal'
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
            logging.debug("Bot démarré avec succès (Premium)")
            self.controller.run()
            logging.debug("Méthode run() de MainController appelée")
            QMessageBox.information(self, "Fin du bot", "Le bot a terminé son exécution.")
        except Exception as e:
            logging.error(f"Erreur lors de l'exécution du bot: {e}")
            QMessageBox.critical(self, "Erreur critique", f"Une erreur est survenue : {e}")

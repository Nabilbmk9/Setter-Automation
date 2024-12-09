# config/configuration_manager.py

import json
import os
import logging
from utils.crypto_utils import (
    encrypt_linkedin_password,
    decrypt_linkedin_password,
    encrypt_license_key,
    decrypt_license_key
)
from utils.utils import get_resource_path


class ConfigurationManager:
    def __init__(self, config_file_path=None):
        # Par défaut, utiliser le fichier user_config.json
        if config_file_path is None:
            config_file_path = 'config/user_config.json'
        self.config_file_path = config_file_path
        self.config = self._load_config()

    def _load_config(self):
        """Charge la configuration depuis le fichier JSON."""
        config_path_local = self.config_file_path
        config_path_packaged = get_resource_path(self.config_file_path)

        # Vérifier l'existence du fichier
        if os.path.exists(config_path_local):
            config_path = config_path_local
        elif os.path.exists(config_path_packaged):
            config_path = config_path_packaged
        else:
            logging.error(f"Configuration file {self.config_file_path} not found.")
            return {}

        logging.debug(f"Using config path: {config_path}")

        with open(config_path, 'r') as f:
            config = json.load(f)

        # Si c'est le fichier utilisateur, déchiffrer les données sensibles
        if 'user_config.json' in self.config_file_path:
            self._decrypt_sensitive_data(config)

        return config

    def _decrypt_sensitive_data(self, config):
        """Déchiffre les données sensibles dans la configuration."""
        try:
            if config.get('LINKEDIN_PASSWORD'):
                logging.debug("Decrypting LinkedIn password")
                config['LINKEDIN_PASSWORD'] = decrypt_linkedin_password(config['LINKEDIN_PASSWORD'])
        except Exception as e:
            logging.error(f"Failed to decrypt LINKEDIN_PASSWORD: {e}")
            config['LINKEDIN_PASSWORD'] = ""

        try:
            if config.get('LICENSE_KEY'):
                logging.debug("Decrypting LICENSE_KEY")
                config['LICENSE_KEY'] = decrypt_license_key(config['LICENSE_KEY'])
        except Exception as e:
            logging.error(f"Failed to decrypt LICENSE_KEY: {e}")
            config['LICENSE_KEY'] = ""

    def _encrypt_sensitive_data(self):
        """Chiffre les données sensibles avant de sauvegarder."""
        try:
            if self.config.get('LINKEDIN_PASSWORD'):
                logging.debug("Encrypting LinkedIn password")
                self.config['LINKEDIN_PASSWORD'] = encrypt_linkedin_password(self.config['LINKEDIN_PASSWORD'])
        except Exception as e:
            logging.error(f"Failed to encrypt LINKEDIN_PASSWORD: {e}")
            self.config['LINKEDIN_PASSWORD'] = ""

        try:
            if self.config.get('LICENSE_KEY'):
                logging.debug("Encrypting LICENSE_KEY")
                self.config['LICENSE_KEY'] = encrypt_license_key(self.config['LICENSE_KEY'])
        except Exception as e:
            logging.error(f"Failed to encrypt LICENSE_KEY: {e}")
            self.config['LICENSE_KEY'] = ""

    def get(self, key, default=None):
        """Récupère une valeur dans la configuration."""
        return self.config.get(key, default)

    def update(self, updates):
        """Met à jour la configuration en mémoire."""
        self.config.update(updates)

    def save(self):
        """Sauvegarde la configuration en mémoire dans le fichier."""
        self._encrypt_sensitive_data()

        # Créer le dossier de configuration si nécessaire
        os.makedirs(os.path.dirname(self.config_file_path), exist_ok=True)

        with open(self.config_file_path, 'w') as f:
            json.dump(self.config, f, indent=4)
        logging.debug(f"Configuration saved to {self.config_file_path}")

# config/config.py

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

def load_config(config_file_path=None):
    # Si aucun chemin n'est fourni, utiliser le fichier de configuration utilisateur par défaut
    if config_file_path is None:
        config_file_path = 'config/user_config.json'

    config_path_local = config_file_path
    config_path_packaged = get_resource_path(config_file_path)

    if os.path.exists(config_path_local):
        config_path = config_path_local
    elif os.path.exists(config_path_packaged):
        config_path = config_path_packaged
    else:
        logging.error(f"Configuration file {config_file_path} not found.")
        return {}

    logging.debug(f"Using config path: {config_path}")

    with open(config_path, 'r') as f:
        config = json.load(f)

    # Si on charge le fichier user_config.json, déchiffrer les valeurs sensibles
    if 'user_config.json' in config_file_path:
        # Déchiffrer le mot de passe LinkedIn
        try:
            if config.get('LINKEDIN_PASSWORD'):
                logging.debug("Decrypting LinkedIn password")
                config['LINKEDIN_PASSWORD'] = decrypt_linkedin_password(config['LINKEDIN_PASSWORD'])
        except Exception as e:
            logging.error(f"Failed to decrypt LINKEDIN_PASSWORD: {e}")
            config['LINKEDIN_PASSWORD'] = ""

        # Déchiffrer la clé de licence
        try:
            if config.get('LICENSE_KEY'):
                logging.debug("Decrypting LICENSE_KEY")
                config['LICENSE_KEY'] = decrypt_license_key(config['LICENSE_KEY'])
        except Exception as e:
            logging.error(f"Failed to decrypt LICENSE_KEY: {e}")
            config['LICENSE_KEY'] = ""

    return config

def update_config(new_config):
    # Toujours mettre à jour le fichier user_config.json
    config_file_path = 'config/user_config.json'

    config = load_config(config_file_path)
    config.update(new_config)

    # Chiffrer le mot de passe LinkedIn
    try:
        if config.get('LINKEDIN_PASSWORD'):
            logging.debug("Encrypting LinkedIn password")
            config['LINKEDIN_PASSWORD'] = encrypt_linkedin_password(config['LINKEDIN_PASSWORD'])
    except Exception as e:
        logging.error(f"Failed to encrypt LINKEDIN_PASSWORD: {e}")
        config['LINKEDIN_PASSWORD'] = ""

    # Chiffrer la clé de licence
    try:
        if config.get('LICENSE_KEY'):
            logging.debug("Encrypting LICENSE_KEY")
            config['LICENSE_KEY'] = encrypt_license_key(config['LICENSE_KEY'])
    except Exception as e:
        logging.error(f"Failed to encrypt LICENSE_KEY: {e}")
        config['LICENSE_KEY'] = ""

    # S'assurer que le dossier de configuration existe
    os.makedirs(os.path.dirname(config_file_path), exist_ok=True)

    # Enregistrer la configuration mise à jour
    with open(config_file_path, 'w') as f:
        json.dump(config, f, indent=4)
    logging.debug(f"Configuration in JSON file updated at {config_file_path}")

import json
import os
import logging
import sys
from utils.crypto_utils import encrypt_message, decrypt_message, generate_key, load_key


def get_resource_path(relative_path):
    """Obtenir le chemin absolu d'une ressource, en utilisant `sys._MEIPASS` si disponible."""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# Définir les chemins des fichiers de configuration
CONFIG_FILE_PATH_LOCAL = 'config/user_config.json'
KEY_FILE_PATH_LOCAL = 'config/secret.key'

# Utiliser le chemin relatif correct pour les fichiers empaquetés
CONFIG_FILE_PATH_PACKAGED = get_resource_path('config/user_config.json')
KEY_FILE_PATH_PACKAGED = get_resource_path('config/secret.key')


def ensure_key_exists():
    key_path = KEY_FILE_PATH_LOCAL if os.path.exists(KEY_FILE_PATH_LOCAL) else KEY_FILE_PATH_PACKAGED
    if not os.path.exists(key_path):
        generate_key()


def load_config():
    config_path = CONFIG_FILE_PATH_LOCAL if os.path.exists(CONFIG_FILE_PATH_LOCAL) else CONFIG_FILE_PATH_PACKAGED
    logging.debug(f"Using config path: {config_path}")

    if not os.path.exists(config_path):
        logging.error(f"Configuration file {config_path} not found.")
        return {}

    ensure_key_exists()
    with open(config_path, 'r') as f:
        config = json.load(f)

    # Déchiffrer les valeurs sensibles
    try:
        logging.debug(f"Encrypted password from config: {config.get('LINKEDIN_PASSWORD')}")
        config['LINKEDIN_PASSWORD'] = decrypt_message(config['LINKEDIN_PASSWORD'])
        logging.debug(f"Decrypted password: {config['LINKEDIN_PASSWORD']}")
    except Exception as e:
        logging.error(f"Failed to decrypt LINKEDIN_PASSWORD: {e}")
        config['LINKEDIN_PASSWORD'] = ""

    return config


def update_config(config):
    key_path = KEY_FILE_PATH_LOCAL if os.path.exists(KEY_FILE_PATH_LOCAL) else KEY_FILE_PATH_PACKAGED
    config_path = CONFIG_FILE_PATH_LOCAL if os.path.exists(CONFIG_FILE_PATH_LOCAL) else CONFIG_FILE_PATH_PACKAGED

    ensure_key_exists()
    config['LINKEDIN_PASSWORD'] = encrypt_message(config['LINKEDIN_PASSWORD'])

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    logging.debug(f"Configuration in JSON file updated at {config_path}")

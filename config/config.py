import json
import os
import logging
from utils.crypto_utils import encrypt_message, decrypt_message, generate_key

CONFIG_FILE_PATH = 'config/user_config.json'
KEY_FILE_PATH = 'config/secret.key'


def ensure_key_exists():
    if not os.path.exists(KEY_FILE_PATH):
        generate_key()


def load_config():
    if not os.path.exists(CONFIG_FILE_PATH):
        logging.error(f"Configuration file {CONFIG_FILE_PATH} not found.")
        return {}

    ensure_key_exists()
    with open(CONFIG_FILE_PATH, 'r') as f:
        config = json.load(f)

    # Déchiffrer les valeurs sensibles
    try:
        config['LINKEDIN_PASSWORD'] = decrypt_message(config['LINKEDIN_PASSWORD'])
    except Exception as e:
        logging.error(f"Failed to decrypt LINKEDIN_PASSWORD: {e}")
        config['LINKEDIN_PASSWORD'] = ""

    return config


def update_config(config):
    ensure_key_exists()
    config['LINKEDIN_PASSWORD'] = encrypt_message(config['LINKEDIN_PASSWORD'])

    with open(CONFIG_FILE_PATH, 'w') as f:
        json.dump(config, f, indent=4)
    logging.debug("Configuration in JSON file updated")

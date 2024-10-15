# utils/crypto_utils.py

from cryptography.fernet import Fernet
import base64
import os
import logging

# Chemins des fichiers de clés
LICENSE_KEY_FILE_PATH = "config/license_secret.key"
PASSWORD_KEY_FILE_PATH = "config/password_secret.key"


def generate_key(key_file_path):
    if not os.path.exists(os.path.dirname(key_file_path)):
        os.makedirs(os.path.dirname(key_file_path))
    key = Fernet.generate_key()
    with open(key_file_path, "wb") as key_file:
        key_file.write(key)
    logging.debug(f"Generated new encryption key at {key_file_path}")


def load_key(key_file_path):
    if not os.path.exists(key_file_path):
        generate_key(key_file_path)
    with open(key_file_path, "rb") as key_file:
        key = key_file.read()
    logging.debug(f"Loaded encryption key from {key_file_path}")
    return key


def encrypt_message(message: str, key_file_path: str) -> str:
    key = load_key(key_file_path)
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    logging.debug(f"Encrypted message with key from {key_file_path}")
    return base64.urlsafe_b64encode(encrypted_message).decode()


def decrypt_message(encrypted_message: str, key_file_path: str) -> str:
    try:
        key = load_key(key_file_path)
        f = Fernet(key)
        logging.debug(f"Decrypting message with key from {key_file_path}")
        decoded_message = base64.urlsafe_b64decode(encrypted_message.encode())
        decrypted_message = f.decrypt(decoded_message)
        logging.debug(f"Decrypted message")
        return decrypted_message.decode()
    except Exception as e:
        logging.error(f"Error decrypting message: {e}", exc_info=True)
        raise


# Fonctions spécifiques pour le mot de passe LinkedIn
def encrypt_linkedin_password(password: str) -> str:
    return encrypt_message(password, PASSWORD_KEY_FILE_PATH)


def decrypt_linkedin_password(encrypted_password: str) -> str:
    return decrypt_message(encrypted_password, PASSWORD_KEY_FILE_PATH)


# Fonctions spécifiques pour la clé de licence
def encrypt_license_key(license_key: str) -> str:
    return encrypt_message(license_key, LICENSE_KEY_FILE_PATH)


def decrypt_license_key(encrypted_license_key: str) -> str:
    return decrypt_message(encrypted_license_key, LICENSE_KEY_FILE_PATH)

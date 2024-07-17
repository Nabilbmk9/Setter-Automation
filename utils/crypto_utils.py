from cryptography.fernet import Fernet
import base64
import os
import logging

KEY_FILE_PATH = "config/secret.key"


# Générer une clé et l'enregistrer dans un fichier
def generate_key():
    if not os.path.exists(os.path.dirname(KEY_FILE_PATH)):
        os.makedirs(os.path.dirname(KEY_FILE_PATH))
    key = Fernet.generate_key()
    with open(KEY_FILE_PATH, "wb") as key_file:
        key_file.write(key)
    logging.debug(f"Generated new encryption key: {key}")


# Charger la clé
def load_key():
    if not os.path.exists(KEY_FILE_PATH):
        generate_key()
    key = open(KEY_FILE_PATH, "rb").read()
    logging.debug(f"Loaded encryption key")
    return key


# Chiffrer un message
def encrypt_message(message: str) -> str:
    key = load_key()
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    logging.debug(f"Encrypted message")
    return base64.urlsafe_b64encode(encrypted_message).decode()


# Déchiffrer un message
def decrypt_message(encrypted_message: str) -> str:
    try:
        key = load_key()
        f = Fernet(key)
        logging.debug(f"Decrypting message...")
        decoded_message = base64.urlsafe_b64decode(encrypted_message.encode())
        decrypted_message = f.decrypt(decoded_message)
        logging.debug(f"Decrypted message")
        return decrypted_message.decode()
    except Exception as e:
        logging.error(f"Error decrypting message: {e}", exc_info=True)
        raise

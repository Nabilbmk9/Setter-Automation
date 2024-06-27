from cryptography.fernet import Fernet
import base64
import os
import logging

KEY_FILE_PATH = "secret.key"

# Générer une clé et l'enregistrer dans un fichier
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE_PATH, "wb") as key_file:
        key_file.write(key)
    logging.debug("Generated new encryption key")

# Charger la clé
def load_key():
    if not os.path.exists(KEY_FILE_PATH):
        generate_key()
    key = open(KEY_FILE_PATH, "rb").read()
    logging.debug(f"Loaded encryption key: {key}")
    return key

# Chiffrer un message
def encrypt_message(message: str) -> str:
    key = load_key()
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    logging.debug(f"Encrypted message: {encrypted_message}")
    return base64.urlsafe_b64encode(encrypted_message).decode()

# Déchiffrer un message
def decrypt_message(encrypted_message: str) -> str:
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(base64.urlsafe_b64decode(encrypted_message.encode()))
    logging.debug(f"Decrypted message: {decrypted_message}")
    return decrypted_message.decode()

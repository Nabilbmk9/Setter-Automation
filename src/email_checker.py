import imaplib
import email
from email.header import decode_header
from datetime import date
import time
import logging
from src.utils import get_env_variable
from data_manager import DataManager

# Configurer le logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_email_credentials():
    email_user = get_env_variable('EMAIL_USER')
    email_password = get_env_variable('EMAIL_PASSWORD')
    return email_user, email_password


def connect_to_email():
    email_user, email_password = get_email_credentials()
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email_user, email_password)
    return mail


def check_for_linkedin_responses(mail, data_manager):
    mail.select('inbox')  # Sélectionner le dossier 'inbox'

    # Rechercher les messages non lus de LinkedIn
    status, messages = mail.search(None, '(UNSEEN FROM "linkedin.com")')
    messages = messages[0].split()  # Séparer les identifiants de messages

    for msg_num in messages:  # Itérer sur chaque message non lu
        status, msg_data = mail.fetch(msg_num, '(RFC822)')  # Récupérer le message complet
        for response_part in msg_data:  # Itérer sur chaque partie du message
            if isinstance(response_part, tuple):  # Vérifier si la partie est un tuple
                msg = email.message_from_bytes(response_part[1])  # Convertir en objet message
                subject, encoding = decode_header(msg['Subject'])[0]  # Décoder l'en-tête 'Subject'
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else 'utf-8')  # Décoder le sujet si nécessaire
                if 'LinkedIn' in subject:  # Filtrer les emails LinkedIn
                    for part in msg.walk():  # Parcourir les parties du message
                        if part.get_content_type() == 'text/plain':  # Filtrer les parties en texte brut
                            message_text = part.get_payload(decode=True).decode('utf-8')  # Décoder le texte du message
                            name = extract_name_from_message(message_text)  # Extraire le nom de l'expéditeur
                            if name:  # Si un nom est extrait
                                data_manager.mark_message_as_responded(name)  # Mettre à jour la base de données
                                logger.info(f"Réponse détectée et enregistrée pour : {name}")  # Enregistrer un log
    return None  # Retour de la fonction


def extract_name_from_message(message_text):
    """
    Extrait le nom de l'expéditeur à partir du texte du message LinkedIn.
    """
    lines = message_text.splitlines()
    for line in lines:
        if 'vient de vous envoyer un message' in line:
            # Extraire le nom avant "vient de vous envoyer un message"
            name = line.split(' vient de vous envoyer un message')[0].strip()
            return name
    return None


def run_email_checker():
    data_manager = DataManager(db_path='linkedin_contacts.db')
    mail = connect_to_email()
    while True:
        check_for_linkedin_responses(mail, data_manager)
        time.sleep(300)  # Vérifie les emails toutes les 5 minutes

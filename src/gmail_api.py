import base64
import re
import os.path
import logging
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.data_manager import DataManager
from src.utils import remove_emojis

# Configurer le logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Portée de l'API Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']


def get_gmail_service():
    """Connecte à l'API Gmail et retourne le service."""
    creds = None
    # Le fichier token.json stocke les jetons d'accès et de mise à jour de l'utilisateur
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Si aucun jeton n'est disponible, laissez l'utilisateur se connecter.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Enregistrez les jetons pour la prochaine exécution
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Appeler l'API Gmail
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        logger.error(f'An error occurred: {error}')


def check_for_linkedin_responses(service, data_manager):
    """Vérifie les réponses LinkedIn dans les emails non lus et les marque comme lus après traitement."""
    try:
        # Requête pour les emails non lus de LinkedIn
        results = service.users().messages().list(userId='me', q='is:unread from:messaging-digest-noreply@linkedin.com').execute()
        messages = results.get('messages', [])

        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()

            # Affichez les en-têtes du message
            headers = msg.get('payload', {}).get('headers', [])
            from_value = None
            for header in headers:
                if header['name'] == 'From':
                    from_value = header['value']

            if from_value:
                if "via LinkedIn" in from_value:
                    name = extract_name_from_header(from_value)
                    if name:
                        cleaned_name = remove_emojis(name).strip()
                        data_manager.mark_message_as_responded(cleaned_name)
                elif "Messagerie LinkedIn" in from_value:
                    # Lire le contenu de l'email
                    for part in msg.get('payload', {}).get('parts', []):
                        if part['mimeType'] == 'text/plain':
                            message_text = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                            names = extract_names_from_email_content(message_text)
                            for name in names:
                                cleaned_name = remove_emojis(name).strip()
                                data_manager.mark_message_as_responded(cleaned_name)

            # Marquer le message comme lu
            service.users().messages().modify(
                userId='me',
                id=message['id'],
                body={'removeLabelIds': ['UNREAD']}
            ).execute()

    except HttpError as error:
        logger.error(f'An error occurred: {error}')


def extract_name_from_header(from_header):
    """Extrait le nom de l'expéditeur de l'en-tête 'From'."""
    if '<' in from_header:
        name_part = from_header.split('<')[0].strip()
        # Supprimer "via LinkedIn" si présent
        name_part = name_part.replace(' via LinkedIn', '').strip()
        return name_part
    return None


def extract_names_from_email_content(content):
    """Extrait les noms du contenu de l'email."""
    names = re.findall(r'^([A-Z][a-zA-Z\s\-\’\'\.]+) \(', content, re.MULTILINE)
    return names


def run_email_checker():
    """Exécute le vérificateur d'emails."""
    data_manager = DataManager(db_path='linkedin_contacts.db')
    service = get_gmail_service()
    while True:
        check_for_linkedin_responses(service, data_manager)
        logger.info('No new message, waiting for 5 minutes before retrying.')
        time.sleep(300)  # Vérifie les emails toutes les 5 minutes

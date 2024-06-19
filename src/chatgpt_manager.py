from utils import get_env_variable
import openai
import logging

# Configurer le logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatGPTManager:
    def __init__(self, api_key=None):
        self.api_key = api_key or get_env_variable('GPT_API_KEY')
        openai.api_key = self.api_key

    def generate_custom_message(self, profile_info):
        prompt = (
            f"Tu es un assistant de rédaction spécialisé dans les messages LinkedIn. "
            f"Ta tâche est de rédiger un message court et personnalisé (max 299 caractères) pour contacter un développeur en reconversion professionnelle. "
            f"Voici les informations du profil :\n\n"
            f"Nom complet : {profile_info['full_name']}\n"
            f"Prénom : {profile_info['first_name']}\n"
            f"Nom : {profile_info['last_name']}\n"
            f"Expérience professionnelle : {profile_info.get('experience', 'Non spécifié')}\n"
            f"Compétences : {profile_info.get('skills', 'Non spécifié')}\n\n"
            f"Voici un exemple de message actuel qui fonctionne bien :\n\n"
            f"\"Salut {{first_name}}, je te contacte parce que moi aussi j'ai fait une reconversion professionnelle. "
            f"Aujourd'hui, je suis développeur freelance. Je sais que ça peut être difficile de se démarquer au début pour trouver son premier CDI ou sa première mission freelance. "
            f"Est-ce que c'est ton cas ?\"\n\n"
            f"En utilisant les informations fournies et en t'inspirant du message actuel, écris un message personnalisé pour ce profil :"
        )

        try:
            response = openai.Completion.create(
                model="text-davinci-003",  # Choisissez le moteur approprié
                prompt=prompt,
                max_tokens=150,
                temperature=0.7,  # Ajustez la température pour des réponses plus variées
                top_p=1.0,
                n=1,  # Nombre de complétions à générer
                frequency_penalty=0.5,
                presence_penalty=0.0,
                stop=["\n\n"]  # Arrête la génération après deux nouvelles lignes
            )
            message = response.choices[0].text.strip()
            logger.info(f"Message personnalisé généré : {message}")
            return message
        except Exception as e:
            logger.error(f"Erreur lors de la génération du message personnalisé : {e}")
            return None

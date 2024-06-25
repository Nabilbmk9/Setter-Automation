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

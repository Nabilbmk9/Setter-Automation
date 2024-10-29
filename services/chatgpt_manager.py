# services/chatgpt_manager.py

from openai import OpenAI, OpenAIError
import logging


class ChatGPTManager:
    def __init__(self, api_key, prompt_template):
        self.api_key = api_key
        self.prompt_template = prompt_template
        self.client = OpenAI(api_key=self.api_key)

    def generate_response(self, prompt):
        """Génère une réponse en utilisant ChatGPT avec le prompt fourni."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            # Accéder au contenu de la réponse
            return response.choices[0].message.content.strip()
        except OpenAIError as e:
            logging.error(f"Erreur avec l'API OpenAI : {e}")
            return None
        except Exception as e:
            logging.error(f"Erreur inattendue lors de la génération de la réponse : {e}")
            return None

    @classmethod
    def validate_api_key(cls, api_key):
        """Valide la clé API en faisant un appel test à OpenAI."""
        try:
            client = OpenAI(api_key=api_key)
            # Appel simple pour vérifier la validité de la clé API
            client.models.list()
            return True
        except OpenAIError as e:
            logging.error(f"Erreur de validation de la clé API : {e}")
            return False
        except Exception as e:
            logging.error(f"Erreur inattendue lors de la validation de la clé API : {e}")
            return False

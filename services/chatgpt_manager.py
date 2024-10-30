# services/chatgpt_manager.py

from openai import OpenAI, OpenAIError
import logging


class ChatGPTManager:
    def __init__(self, api_key, prompt_template, relevance_prompt_template=None):
        self.api_key = api_key
        self.prompt_template = prompt_template
        self.relevance_prompt_template = relevance_prompt_template
        self.client = OpenAI(api_key=self.api_key)

    def generate_response(self, prompt_variables):
        """Génère une réponse en utilisant ChatGPT avec les variables du prompt."""
        # Remplacer les variables dans le prompt des messages
        prompt = self.prompt_template.format(**prompt_variables)

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

    def evaluate_profile_relevance(self, profile_data):
        """Évalue la pertinence d'un profil en utilisant ChatGPT."""
        if not self.relevance_prompt_template:
            logging.error("Le prompt d'analyse des profils n'est pas défini.")
            return None

        # Remplacer les variables dans le prompt d'analyse des profils
        prompt = self.relevance_prompt_template.format(**profile_data)

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
            logging.error(f"Erreur inattendue lors de l'évaluation du profil : {e}")
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

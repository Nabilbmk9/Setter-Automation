# services/chatgpt_manager.py

from openai import OpenAI, OpenAIError, AssistantEventHandler
import logging


class ChatGPTManager:
    def __init__(self, api_key, prompt_template=None, relevance_prompt_template=None):
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

    # --- Méthodes pour l'intégration de l'assistant GPT ---

    def create_thread(self):
        """Crée un nouveau thread pour la conversation."""
        try:
            thread = self.client.beta.threads.create()
            return thread.id
        except OpenAIError as e:
            logging.error(f"Erreur lors de la création du thread : {e}")
            return None

    def add_message_to_thread(self, thread_id, message_content):
        """Ajoute un message utilisateur au thread."""
        try:
            message = self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message_content
            )
            return message.id
        except OpenAIError as e:
            logging.error(f"Erreur lors de l'ajout du message : {e}")
            return None

    def run_assistant(self, thread_id, assistant_id):
        """Exécute l'assistant sur le thread pour obtenir une réponse."""
        try:
            run = self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id
            )
            return run.id
        except OpenAIError as e:
            logging.error(f"Erreur lors de l'exécution de l'assistant : {e}")
            return None

    def get_assistant_response(self, thread_id):
        """Récupère la dernière réponse de l'assistant."""
        try:
            messages = self.client.beta.threads.messages.list(thread_id=thread_id)
            # Récupérer le dernier message de l'assistant
            for message in reversed(messages.data):
                if message.role == 'assistant':
                    return message.content
            return None
        except OpenAIError as e:
            logging.error(f"Erreur lors de la récupération de la réponse : {e}")
            return None

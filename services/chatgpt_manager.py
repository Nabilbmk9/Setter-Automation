# services/chatgpt_manager.py
import time

from openai import OpenAI, OpenAIError, AssistantEventHandler
import logging


class ChatGPTManager:
    def __init__(self, api_key, relevance_prompt_template=None):
        self.api_key = api_key
        self.relevance_prompt_template = relevance_prompt_template
        self.client = OpenAI(api_key=self.api_key)

    # def generate_response(self, prompt_variables):
    #     """Génère une réponse en utilisant ChatGPT avec les variables du prompt."""
    #     # Remplacer les variables dans le prompt des messages
    #     prompt = self.prompt_template.format(**prompt_variables)
    #
    #     try:
    #         response = self.client.chat.completions.create(
    #             model="gpt-3.5-turbo",
    #             messages=[{"role": "user", "content": prompt}]
    #         )
    #         # Accéder au contenu de la réponse
    #         return response.choices[0].message.content.strip()
    #     except OpenAIError as e:
    #         logging.error(f"Erreur avec l'API OpenAI : {e}")
    #         return None
    #     except Exception as e:
    #         logging.error(f"Erreur inattendue lors de la génération de la réponse : {e}")
    #         return None

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

    def check_message_relevance(self, conversation_history):
        """Vérifie si la conversation est pertinente pour une réponse automatique."""
        prompt = (
                "Voici l'historique d'une conversation :\n\n"
                + "\n".join([f"{msg['author']}: {msg['message']}" for msg in conversation_history])
                + "\n\nEst ce que la conversation est coherente ?  Répondez uniquement par 'oui' ou 'non' avec une petite explication tres très courte de ton choix."
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip().lower()  # 'oui' ou 'non'
        except OpenAIError as e:
            logging.error(f"Erreur lors de la vérification de la pertinence du message : {e}")
            return "non"  # Par défaut, renvoyer 'non' en cas d'erreur

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
                    return message.content[0].text.value
            return None
        except OpenAIError as e:
            logging.error(f"Erreur lors de la récupération de la réponse : {e}")
            return None

    # Ce code est utilisé seulement pour les tests
    def get_thread_content(self, thread_id):
        """Récupère tout le contenu actuel du thread pour vérification."""
        try:
            messages = self.client.beta.threads.messages.list(thread_id=thread_id)
            return [msg.content for msg in messages.data if msg.role in ['user', 'assistant']]
        except OpenAIError as e:
            logging.error(f"Erreur lors de la récupération du contenu du thread : {e}")
            return []

    def generate_response_with_assistant(self, assistant_id, profile_data):
        """Génère une réponse en utilisant l'assistant via assistant ID avec les données de profil."""
        try:
            thread_id = self.create_thread()
            if not thread_id:
                logging.error("Échec de la création du thread.")
                return None

            # Préparer le message avec les données du profil
            message_content = self.format_profile_data(profile_data)
            if not message_content:
                logging.error("Échec de la préparation des données du profil.")
                return None

            # Ajouter le message au thread
            self.add_message_to_thread(thread_id, message_content)

            # Exécuter l'assistant
            run_id = self.run_assistant(thread_id, assistant_id)
            if not run_id:
                logging.error("Échec de l'exécution de l'assistant.")
                return None

            # Attendre que l'assistant ait terminé de générer la réponse
            time.sleep(5)

            # Récupérer la réponse de l'assistant
            assistant_response = self.get_assistant_response(thread_id)
            if assistant_response:
                return assistant_response
            else:
                logging.error("Aucune réponse de l'assistant.")
                return None

        except Exception as e:
            logging.error(f"Erreur lors de la génération de la réponse avec l'assistant : {e}")
            return None

    def format_profile_data(self, profile_data):
        """Formate les données du profil en un message pour l'assistant."""
        try:
            message = (
                f"Voici les informations du profil:\n"
                f"Prénom: {profile_data.get('first_name', '')}\n"
                # f"Nom: {profile_data.get('last_name', '')}\n"
                # f"Nom complet: {profile_data.get('full_name', '')}\n"
                f"Titre: {profile_data.get('title', '')}\n"
                # f"Entreprise: {profile_data.get('company', '')}\n"
                f"Informations: {profile_data.get('info', '')}\n"
                # f"Expérience: {profile_data.get('experience', '')}\n"
                # f"Position: {profile_data.get('position', '')}\n"
            )
            return message
        except Exception as e:
            logging.error(f"Erreur lors du formatage des données du profil : {e}")
            return None

from config import get_env_variable
import openai


class ChatGPTManager:
    def __init__(self, api_key):
        self.api_key = get_env_variable('GPT_KEY')
        self.client = openai.OpenAI(api_key=api_key)

    def send_message(self, message):
        # Intégration avec l'API de ChatGPT pour envoyer un message
        pass



from config import get_env_variable


class ChatGPTManager:
    def __init__(self, api_key):
        self.api_key = get_env_variable('GPT_KEY')

    def send_message(self, message):
        # Intégration avec l'API de ChatGPT pour envoyer un message
        pass



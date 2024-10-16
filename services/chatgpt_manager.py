from openai import OpenAI, OpenAIError


class ChatGPTManager:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def generate_response(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            # Accéder au contenu de la réponse
            return response.choices[0].message.content
        except OpenAIError as e:
            print(f"Erreur avec l'API OpenAI : {e}")
            return None

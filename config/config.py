from dotenv import load_dotenv, set_key, find_dotenv
import os


def load_config():
    load_dotenv()
    config = {
        'LINKEDIN_EMAIL': os.getenv('LINKEDIN_EMAIL', ''),
        'LINKEDIN_PASSWORD': os.getenv('LINKEDIN_PASSWORD', ''),
        'LINKEDIN_SEARCH_LINK': os.getenv('LINKEDIN_SEARCH_LINK', ''),
        'MESSAGE_A': os.getenv('MESSAGE_A', ''),
        'MESSAGE_B': os.getenv('MESSAGE_B', ''),
        'GPT_API_KEY': os.getenv('GPT_API_KEY', ''),
        'MESSAGES_PER_DAY': os.getenv('MESSAGES_PER_DAY', '10')
    }
    return config

def update_config(config):
    env_path = find_dotenv()
    for key, value in config.items():
        set_key(env_path, key, value)

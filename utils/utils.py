import json
import os
import sys
import re
import urllib.parse


def extract_keywords_from_search_link(search_link):
    parsed_url = urllib.parse.urlparse(search_link)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    keywords = query_params.get('keywords', [''])[0]
    return keywords


def get_next_message(message_a, message_b, toggle):
    """Alterner entre message A et B. Si l'un des messages est vide, utiliser l'autre message."""
    if message_a and message_b:
        toggle = not toggle
        return (message_a if toggle else message_b), toggle
    return (message_a or message_b), toggle


def remove_emojis(data):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese characters
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', data)


def get_resource_path(relative_path):
    """Obtenir le chemin absolu d'une ressource, en utilisant `sys._MEIPASS` si disponible."""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_path, relative_path)


def get_version_from_config():
    config_path = os.path.join("config", "app_config.json")
    try:
        with open(config_path, "r") as config_file:
            config_data = json.load(config_file)
            return config_data.get("current_version", "Unknown Version")
    except FileNotFoundError:
        return "Version file not found"
    except json.JSONDecodeError:
        return "Invalid JSON"


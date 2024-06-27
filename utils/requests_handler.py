import requests


def fetch_announcement(announcement_url):
    try:
        response = requests.get(announcement_url)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return ""
    except Exception as e:
        print(f"Erreur lors de la récupération des annonces : {e}")
        return ""


def check_for_updates(current_version, version_url):
    try:
        response = requests.get(version_url)
        if response.status_code == 200:
            latest_version = response.text.strip()
            return latest_version != current_version, latest_version
        else:
            return False, current_version
    except Exception as e:
        print(f"Erreur lors de la vérification des mises à jour : {e}")
        return False, current_version

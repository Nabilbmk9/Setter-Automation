import requests


def fetch_announcement():
    url = "https://storage.googleapis.com/linkedin-automation-updates/annoucement.txt"


    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return ""
    except Exception as e:
        print(f"Erreur lors de la récupération des annonces : {e}")
        return ""


def check_for_updates(current_version):
    url = "https://storage.googleapis.com/linkedin-automation-updates/version.txt"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            latest_version = response.text.strip()
            return latest_version != current_version, latest_version
        else:
            return False, current_version
    except Exception as e:
        print(f"Erreur lors de la vérification des mises à jour : {e}")
        return False, current_version

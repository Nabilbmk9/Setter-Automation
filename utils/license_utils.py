# utils/license_utils.py
import requests
import logging


def verify_license(license_key):
    """Vérifie la validité de la clé de licence."""
    try:
        response = requests.post(
            'https://licences-gen-bot.ew.r.appspot.com/verify_license',
            json={"license_key": license_key},
            timeout=10  # Ajouter un timeout pour éviter les blocages
        )
        response.raise_for_status()
        data = response.json()
        valid = data.get('valid', False)
        return valid
    except requests.exceptions.Timeout:
        logging.error("Timeout lors de la vérification de la licence.")
        return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur de connexion lors de la vérification de la licence: {e}")
        return False

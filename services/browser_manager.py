# browser_manager.py
from playwright.sync_api import sync_playwright
import os
import sys
import platform


class BrowserManager:
    def __init__(self, headless=False, block_images=False):
        self.playwright = sync_playwright().start()

        # Détecter le système d'exploitation
        os_name = platform.system()

        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Construire le chemin du navigateur en fonction du répertoire d'installation
        if hasattr(sys, '_MEIPASS'):
            # Si nous sommes dans un environnement empaqueté par PyInstaller
            base_dir = os.path.join(sys._MEIPASS, '_internal', 'ms-playwright')
        else:
            # Sinon, utiliser le chemin de développement normal
            base_dir = os.path.join(base_dir, '..', 'ms-playwright')

        # Chemin du fichier exécutable Chromium en fonction du système
        if os_name == 'Windows':
            chromium_path = os.path.join(base_dir, 'chromium-1112', 'chrome-win', 'chrome.exe')
        elif os_name == 'Darwin':  # macOS
            chromium_path = os.path.join(base_dir, 'chromium-1112', 'chrome-mac', 'Chromium.app', 'Contents', 'MacOS', 'Chromium')
        else:
            raise NotImplementedError(f"Système d'exploitation non pris en charge : {os_name}")

        # Lancer le navigateur avec le chemin approprié
        self.browser = self.playwright.chromium.launch(
            headless=headless,
            executable_path=chromium_path
        )
        self.context = self.browser.new_context()
        if block_images:
            self._setup_request_interception()

    def _setup_request_interception(self):
        # Définir une route pour intercepter les requêtes
        self.context.route('**/*', self._route_intercept)

    def _route_intercept(self, route):
        # Bloquer les images pour améliorer la performance
        if route.request.resource_type == "image":
            route.abort()
        else:
            route.continue_()

    def new_page(self):
        return self.context.new_page()

    def close(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()

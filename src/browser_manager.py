from playwright.sync_api import sync_playwright


class BrowserManager:
    def __init__(self, headless=False, block_images=False):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
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

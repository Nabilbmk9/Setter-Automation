import pytest
from unittest.mock import patch, MagicMock

from controllers.main_controller import MainController


@pytest.fixture
def controller():
    with patch('controllers.main_controller.DataManager') as MockDataManager, \
            patch('controllers.main_controller.BrowserManager') as MockBrowserManager, \
            patch('controllers.main_controller.LinkedInScraper') as MockLinkedInScraper:
        # Mocks des dépendances
        mock_data_manager = MockDataManager.return_value
        mock_browser_manager = MockBrowserManager.return_value
        mock_scraper = MockLinkedInScraper.return_value

        # Instanciation de MainController avec des valeurs de test
        controller = MainController(
            username="test_user",
            password="test_password",
            search_link="https://linkedin.com/search",
            messages_per_day=10,
            message_a="Hello {first_name}",
            message_b="Hi {first_name}",
            message_type='normal'
        )

        yield controller, mock_data_manager, mock_browser_manager, mock_scraper


def test_initialization(controller):
    # Déballer la fixture pour accéder au contrôleur et aux mocks
    controller, mock_data_manager, mock_browser_manager, mock_scraper = controller

    # Vérifier les valeurs d'initialisation
    assert controller.username == "test_user"
    assert controller.password == "test_password"
    assert controller.search_link == "https://linkedin.com/search"
    assert controller.messages_per_day == 10
    assert controller.message_a == "Hello {first_name}"
    assert controller.message_b == "Hi {first_name}"
    assert controller.chatgpt_manager is None  # Aucun manager de ChatGPT fourni

    # Vérifier que les mocks ont été assignés correctement
    assert controller.data_manager == mock_data_manager


@pytest.fixture
def controller_with_mocks():
    with patch('controllers.main_controller.DataManager') as MockDataManager, \
            patch('controllers.main_controller.BrowserManager') as MockBrowserManager, \
            patch('controllers.main_controller.LinkedInScraper') as MockLinkedInScraper:
        # Configurer les mocks
        mock_data_manager = MockDataManager.return_value
        mock_browser_manager = MockBrowserManager.return_value
        mock_scraper = MockLinkedInScraper.return_value

        # Création d'une instance du contrôleur avec auto_reply_enabled désactivé pour simplifier le test
        controller = MainController(
            username="test_user",
            password="test_password",
            search_link="https://linkedin.com/search",
            messages_per_day=10,
            message_a="Hello {first_name}",
            message_b="Hi {first_name}",
            message_type='normal',
            auto_reply_enabled=False  # Désactivé pour ce test
        )

        # Associer le mock scraper au contrôleur pour éviter de lancer un navigateur réel
        controller.browser_manager = mock_browser_manager
        controller.scraper = mock_scraper

        yield controller, mock_browser_manager, mock_scraper


def test_run(controller_with_mocks):
    controller, mock_browser_manager, mock_scraper = controller_with_mocks

    # Configurer les mocks pour la méthode `run`
    mock_scraper.login.return_value = None
    mock_scraper.ensure_authenticated.return_value = None
    mock_scraper.init_labels_from_language.return_value = None
    controller.run_prospecting = MagicMock()  # Mock de run_prospecting pour vérifier son appel

    # Exécution de la méthode `run`
    controller.run()

    # Vérifications des appels
    mock_scraper.login.assert_called_once_with("test_user", "test_password")
    mock_scraper.ensure_authenticated.assert_called_once()
    mock_scraper.init_labels_from_language.assert_called_once()
    controller.run_prospecting.assert_called_once()  # Assure-toi que la prospection est lancée

    # Vérifier la fermeture du navigateur
    mock_browser_manager.close.assert_called_once()

import logging
import os
import json
import platform


def get_log_file_path():
    system = platform.system()
    if system == 'Windows':
        appdata_dir = os.getenv('APPDATA')
        log_dir = os.path.join(appdata_dir, 'linkedin_automation_bot')
    elif system == 'Darwin':  # macOS
        appdata_dir = os.path.expanduser('~/Library/Application Support')
        log_dir = os.path.join(appdata_dir, 'linkedin_automation_bot')
    else:  # Linux et autres systèmes Unix
        appdata_dir = os.path.expanduser('~/.local/share')
        log_dir = os.path.join(appdata_dir, 'linkedin_automation_bot')

    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'app.log')
    return log_file


def load_app_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app_config.json')
    with open(config_path, 'r') as f:
        return json.load(f)


def setup_logging():
    app_config = load_app_config()
    debug_mode = app_config.get('debug_mode', False)

    if debug_mode:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    else:
        log_file = get_log_file_path()
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    logger = logging.getLogger(__name__)
    return logger

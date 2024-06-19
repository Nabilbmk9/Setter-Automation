from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit
from main_controller import MainController
from src.utils import get_env_variable
import threading


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bot Application")

        layout = QVBoxLayout()

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        self.start_button = QPushButton("Start Bot")
        self.start_button.clicked.connect(self.start_bot)
        layout.addWidget(self.start_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.bot_running = False
        self.bot_thread = None
        self.controller = None

    def start_bot(self):
        if not self.bot_running:
            self.bot_running = True
            self.controller = MainController(
                username=get_env_variable('LINKEDIN_EMAIL'),
                password=get_env_variable('LINKEDIN_PASSWORD'),
                search_link=get_env_variable('LINKEDIN_SEARCH_LINK'),
                message_a=get_env_variable('MESSAGE_A'),
                message_b=get_env_variable('MESSAGE_B'),
                api_key=get_env_variable('GPT_API_KEY'),
                messages_per_day=int(get_env_variable('MESSAGES_PER_DAY', 10))
            )
            self.bot_thread = threading.Thread(target=self.controller.run)
            self.bot_thread.start()
            self.start_button.setEnabled(False)
            self.log_output.append("Bot started")  # Ajouter le message de log


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

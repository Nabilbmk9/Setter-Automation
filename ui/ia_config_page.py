from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPlainTextEdit, QPushButton, QHBoxLayout


class IAConfigPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.api_key_edit = QLineEdit()
        self.assistant_settings = QPlainTextEdit()
        self.prompt_settings = QPlainTextEdit()

        self.btn_enregistrer = QPushButton("Enregistrer")
        self.btn_annuler = QPushButton("Annuler")

        form_layout = QFormLayout()
        form_layout.addRow("API Key :", self.api_key_edit)
        form_layout.addRow("Paramètres de l'assistant IA :", self.assistant_settings)
        form_layout.addRow("Prompts :", self.prompt_settings)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_enregistrer)
        btn_layout.addWidget(self.btn_annuler)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

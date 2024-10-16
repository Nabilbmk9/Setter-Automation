# message_edit_dialog.py

from PySide6.QtWidgets import QDialog, QTextEdit, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt


class MessageEditDialog(QDialog):
    def __init__(self, title, initial_text):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(400, 350)
        self.max_length = 300

        # Zone de texte pour éditer le message
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(initial_text)
        self.text_edit.textChanged.connect(self.update_character_count)

        # Label pour le compteur de caractères
        self.char_count_label = QLabel()
        self.char_count_label.setAlignment(Qt.AlignRight)
        self.char_count_label.setFont(QFont("Montserrat", 10))
        self.update_character_count()  # Initialiser le compteur

        # Bouton pour enregistrer le message
        self.save_button = QPushButton("Enregistrer")
        self.save_button.clicked.connect(self.accept)
        self.save_button.setFont(QFont("Montserrat", 10))

        # Mise en page de la boîte de dialogue
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.char_count_label)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def update_character_count(self):
        current_length = len(self.text_edit.toPlainText())
        if current_length > self.max_length:
            self.char_count_label.setStyleSheet("color: red;")
        else:
            self.char_count_label.setStyleSheet("color: white;")

        self.char_count_label.setText(f"{current_length}/{self.max_length} caractères")

    def get_text(self):
        return self.text_edit.toPlainText()

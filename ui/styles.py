def get_stylesheet():
    return """
        QMainWindow {
            background-color: #0c1021;
        }
        QLabel {
            color: white;
            font-size: 16px;
            font-weight: bold;
        }
        QLabel#title {
            font-size: 24px;
            margin-bottom: 20px;
        }
        QLabel#version {
            font-size: 12px;
            font-weight: normal;
        }
        QLineEdit {
            background-color: #243672;
            color: white;
            border: 2px solid #7a3ef3;
            border-radius: 10px;
            padding: 5px;
            margin-bottom: 10px;
        }
        /* Style pour les QRadioButton */
        QRadioButton {
            color: white;
            font-size: 12px;
            spacing: 6px;
        }
        QRadioButton::indicator {
            width: 16px;
            height: 16px;
        }

        QRadioButton::indicator::unchecked {
            border: 2px solid #7a3ef3;
            background-color: transparent;
            border-radius: 8px;
        }

        QRadioButton::indicator::checked {
            border: 2px solid #7a3ef3;
            background-color: #7a3ef3;
            border-radius: 8px;
        }

        /* Style pour QCheckBox pour basculer l'analyse des profils */
        QCheckBox {
            color: white;
            font-size: 12px;
            spacing: 6px;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
        }
        QCheckBox::indicator:unchecked {
            border: 2px solid #7a3ef3;
            background-color: transparent;
            border-radius: 8px;
        }
        QCheckBox::indicator:checked {
            border: 2px solid #7a3ef3;
            background-color: #7a3ef3;
            border-radius: 8px;
        }

        /* Style pour les boutons des messages */
        QPushButton#messageButton {
            background-color: #243672;  /* Même couleur que QLineEdit */
            color: white;
            border: 2px solid #7a3ef3;  /* Même bordure que QLineEdit */
            border-radius: 10px;
            padding: 10px;
            padding-left: 15px;  /* Ajouter un padding à gauche */
            font-weight: bold;
            font-size: 14px;
            text-align: left;  /* Alignement du texte à gauche */
        }
        QPushButton#messageButton:hover {
            background-color: #2b3b63;  /* Couleur légèrement plus claire au survol */
        }
        /* Style pour le bouton "Start Bot" */
        QPushButton#startButton {
            background-color: #ff4500;
            color: white;
            border-radius: 10px;
            padding: 10px;
            font-weight: bold;
            font-size: 14px;
            margin-top: 20px;
        }
        QPushButton#startButton:hover {
            background-color: #ff5714;
        }
        QMessageBox {
            background-color: #243672;
            color: white;
        }
        QMessageBox QLabel {
            color: white;
        }
        QMessageBox QPushButton {
            background-color: #ff4500;
            color: white;
            border-radius: 10px;
            padding: 5px;
        }
        QMessageBox QPushButton:hover {
            background-color: #ff5714;
        }
        QDialog {
            background-color: #243672;
        }
        QDialog QLabel {
            color: white;
        }
        QDialog QPushButton {
            background-color: #ff4500;
            color: white;
            border-radius: 10px;
            padding: 5px;
        }
        QDialog QPushButton:hover {
            background-color: #ff5714;
        }
        QTextEdit {
            background-color: #243672;
            color: white;
            border: 2px solid #7a3ef3;
            border-radius: 10px;
            padding: 5px;
        }
    """

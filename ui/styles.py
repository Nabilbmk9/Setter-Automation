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
        QLineEdit {
            background-color: #243672;
            color: white;
            border: 2px solid #7a3ef3;
            border-radius: 10px;
            padding: 5px;
            margin-bottom: 10px;
        }
        QPushButton {
            background-color: #ff4500;
            color: white;
            border-radius: 10px;
            padding: 10px;
            font-weight: bold;
            font-size: 14px;
            margin-top: 20px;
        }
        QPushButton:hover {
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
    """

from PySide6.QtGui import QFont


# === POLICES EN PYTHON === #
def get_default_font():
    """Police par défaut pour les widgets."""
    return QFont("Montserrat", 6)


def get_large_font():
    """Police pour les titres ou labels importants."""
    return QFont("Montserrat", 12)


def get_title_font():
    """Police pour les titres principaux."""
    return QFont("Montserrat", 20)


def get_version_font():
    """Police pour les labels de version."""
    return QFont("Montserrat", 8)


# === FEUILLE DE STYLE CSS === #
def get_stylesheet():
    return """
    /* === GÉNÉRAL === */
    QMainWindow {
        background-color: #0c1021;
    }

    QLabel {
        color: white;
        font-size: 16px; /* Défaut pour les labels */
        font-weight: bold;
    }

    QLabel#title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    QLabel#version {
        font-size: 12px;
        font-weight: normal;
    }

    /* === ZONES DE TEXTE === */
    QLineEdit {
        background-color: #243672;
        color: white;
        border: 2px solid #7a3ef3;
        border-radius: 10px;
        padding: 5px;
        margin-bottom: 10px;
    }

    QTextEdit {
        background-color: #243672;
        color: white;
        border: 2px solid #7a3ef3;
        border-radius: 10px;
        padding: 5px;
    }

    /* === BOUTONS === */
    QPushButton {
        background-color: #243672;
        color: white;
        border: 2px solid #7a3ef3;
        border-radius: 10px;
        padding: 10px;
        font-weight: bold;
        font-size: 14px;
    }

    QPushButton#startButton {
        background-color: #ff4500;
        border-radius: 10px;
        font-size: 16px;
        padding: 10px;
    }

    QPushButton#startButton:hover {
        background-color: #ff5714;
    }
    
    QPushButton#btnEnregistrer {
        background-color: #ff4500;
        color: white;
        border: 2px solid #ff4500;
        border-radius: 20px;
        padding: 10px;
        font-weight: bold;
        font-size: 14px;
    }

    QPushButton#btnEnregistrer:hover {
        background-color: #ff5714;
    }

    QPushButton#btnAnnuler {
        background-color: #7a3ef3;
        color: white;
        border: 2px solid #7a3ef3;
        border-radius: 20px;
        padding: 10px;
        font-weight: bold;
        font-size: 14px;
    }

    QPushButton#btnAnnuler:hover {
        background-color: #9662ff;
    }

    /* === RADIO & CHECKBOX === */
    QRadioButton, QCheckBox {
        color: white;
        font-size: 12px;
    }

    QRadioButton::indicator, QCheckBox::indicator {
        width: 16px;
        height: 16px;
        border: 2px solid #7a3ef3;
        background-color: transparent;
        border-radius: 8px;
    }

    QRadioButton::indicator::checked, QCheckBox::indicator:checked {
        background-color: #7a3ef3;
    }

    /* === MESSAGE BOX === */
    QMessageBox {
        background-color: #243672;
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

    /* === DIALOGUES === */
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

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QLineEdit, QGroupBox, QMessageBox
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import Qt
from db.db import DatabaseManager

class LoginWindow(QMainWindow):
    login_success = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.load_style()
        self.db = DatabaseManager()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        form_container = QWidget()

        form_layout = QVBoxLayout(form_container)

        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Username")

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Password")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        form_layout.addWidget(self.input_username)
        form_layout.addWidget(self.input_password)
        form_layout.addWidget(login_btn)

        form_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addStretch(2)
        main_layout.addWidget(form_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        main_layout.addStretch(2)

    def verify_credentials(self, input_username, input_password):
        credentials = self.db.fetch_all("SELECT * FROM users")[0]
        username, password = credentials[1], credentials[2]
        print(username, password)
        if input_username != username or input_password != password:
            return False
        return True

    def handle_login(self):
        if not self.input_username.text() or not self.input_password.text():
            QMessageBox.critical(self, "Errore", "Inserire i campi")
            return
        
        if not self.verify_credentials(self.input_username.text(), self.input_password.text()):
            QMessageBox.critical(self, "Errore", "Credenziali non valide")
            return
        
        self.login_success.emit()

    def load_style(self):
        with open(r"C:\Users\Vale\gui-example\style\login.qss", "r") as f:
            self.setStyleSheet(f.read())
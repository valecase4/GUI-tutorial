from PyQt6.QtWidgets import QApplication
from components.login import LoginWindow
from components.main_window import MainWindow
from PyQt6.QtGui import QIcon

class WindowManager:
    def __init__(self):
        self.app = QApplication([])
        self.app.setWindowIcon(QIcon("C:/Users/Vale/gui-example/assets/icon.png"))
        self.login_window = LoginWindow()
        self.login_window.showMaximized()
        self.main_window = None

        self.login_window.login_success.connect(self.show_main_window)

    def show_main_window(self):
        self.login_window.close() 
        self.main_window = MainWindow()
        self.main_window.show()

    def run(self):
        self.login_window.show()
        self.app.exec()

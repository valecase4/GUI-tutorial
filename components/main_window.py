from PyQt6.QtWidgets import QMainWindow, QTabWidget
from .exercises_page import ExercisesPage
from .new_exercise_form import NewExerciseForm
from PyQt6.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.showMaximized()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        exercises_page = ExercisesPage()
        new_exercise_form = NewExerciseForm()
        new_exercise_form.added_exercise.connect(exercises_page.refresh_list)

        self.tabs.addTab(exercises_page, QIcon(r"C:\Users\Vale\gui-example\assets\gym.png"), "Esercizi")
        self.tabs.addTab(new_exercise_form, QIcon(r"C:\Users\Vale\gui-example\assets\add.png"), "Aggiungi")

    
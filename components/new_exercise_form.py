from PyQt6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QMessageBox
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt, pyqtSignal
from db.db import DatabaseManager

class NewExerciseForm(QWidget):
    added_exercise = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.load_style()
        self.db = DatabaseManager()
        self.exercises = self.fetch_muscle_groups_from_db()

        form_container = QGroupBox("Aggiungi un esericizio")
        form_container.setMaximumWidth(400)

        form_layout = QVBoxLayout()

        self.exercise_name = QLineEdit()
        self.exercise_name.setMaxLength(30)
        self.exercise_name.setPlaceholderText("Inserisci il nome dell'esercizio")

        self.muscle_group = QComboBox()
        self.muscle_group.addItems([f"{mg[0]},{mg[1]}" for mg in self.exercises])

        submit_button = QPushButton("Salva")
        submit_button.clicked.connect(self.save_exercise_to_db)
        submit_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        form_layout.addWidget(self.exercise_name)
        form_layout.addWidget(self.muscle_group)
        form_layout.addWidget(submit_button)

        form_container.setLayout(form_layout)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(form_container)

        self.setLayout(main_layout)

    def fetch_muscle_groups_from_db(self):
        exercises = self.db.fetch_all("SELECT * FROM muscle_groups")
        return exercises 

    def load_style(self):
        with open(r"C:\Users\Vale\gui-example\style\new_exercise_form.qss", "r") as f:
            self.setStyleSheet(f.read())

    def save_exercise_to_db(self):
        exercise_input = self.exercise_name.text()
        print(exercise_input)
        muscle_group = self.muscle_group.currentText().split(",")[0]
        if not self.verify_exercise_name_input(exercise_input):
            QMessageBox.critical(self, "Errore", "Inserire un nome valido.")
            return
        
        if not self.check_exercise_name_presence_db(exercise_input):
            QMessageBox.critical(self, "Errore", "L'esercizio è già presente nel database")
            return
        self.db.execute_query("""INSERT INTO exercises (name, muscle_group_id) VALUES (?, ?)""", params=(exercise_input, muscle_group))
        QMessageBox.information(self, "Aggiunto", "Esercizio salvato con successo")
        self.exercise_name.clear()
        self.muscle_group.setCurrentIndex(0)
        self.added_exercise.emit()

    def verify_exercise_name_input(self, exercise_name):
        if len(exercise_name) == 0:
            return False
        
        if not self.exercise_name.text().replace(" ", "").isalpha():
            return False
        return True
    
    def check_exercise_name_presence_db(self, exercise_name):
        exercises = [e[1].lower().replace(" ", "") for e in self.db.fetch_all("SELECT * FROM exercises")]

        if exercise_name.lower().replace(" ", "").strip() in exercises:
            return False
        return True
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QHeaderView, QLabel, QPushButton, QHBoxLayout
from db.db import DatabaseManager
from PyQt6.QtCore import Qt, pyqtSignal
from functools import partial

class ExercisesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.exercises = self.fetch_exercises_from_db()
        self.exercises_table = None

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if self.exercises:
            self.exercises_table = ExercisesTable(self.exercises)
            self.listen_delete_signal()
            self.layout.addWidget(self.exercises_table)
        if not self.exercises:
            not_found_exercises = QLabel("Non ci sono esercizi salvati.")
            self.layout.addWidget(not_found_exercises)

        self.setLayout(self.layout)

    def remove_item_from_db(self, item):
        self.db.execute_query("DELETE FROM exercises WHERE name = ?", (item,))
        print(f"{item} removed.")
        self.refresh_list()

    def listen_delete_signal(self):
        if self.exercises_table:
            self.exercises_table.delete_signal.connect(self.remove_item_from_db)

    def fetch_exercises_from_db(self):
        exercises = self.db.fetch_all("""
            SELECT exercises.name, muscle_groups.name 
            FROM exercises 
            JOIN muscle_groups 
            ON exercises.muscle_group_id = muscle_groups.id
        """)
        return exercises
    
    def refresh_list(self):
        print("Update")
        if self.exercises_table:
            self.exercises_table.deleteLater()
        self.exercises = self.fetch_exercises_from_db()
        self.exercises_table = ExercisesTable(self.exercises)
        self.listen_delete_signal()
        self.layout.addWidget(self.exercises_table)


class ExercisesTable(QTableWidget):
    delete_signal = pyqtSignal(str)

    def __init__(self, exercises):
        super().__init__()
        self.exercises = exercises
        self.load_style()

        self.setColumnCount(3)
        self.setRowCount(len(self.exercises))

        self.setHorizontalHeaderLabels(
            [
                "Esercizio",
                "Gruppo Muscolare",
                "Azioni"
            ]
        )

        for i in range(len(self.exercises)):
            for j in range(3):
                if j < 2:
                    label = QLabel()
                    label.setText(f"{self.exercises[i][j]}")
                    label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
                    self.setCellWidget(i, j, label)
                if j == 2:
                    delete_btn = QPushButton("Elimina")

                    container = QWidget()
                    layout = QHBoxLayout(container)

                    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    layout.setContentsMargins(0, 0, 0, 0)
                    
                    delete_btn.setStyleSheet("""
                        background: red;
                        color: white;
                        border: none;
                        font-weight: bold;
                    """)
                    delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                    delete_btn.clicked.connect(partial(self.emit_delete_signal, self.exercises[i][0]))
                    delete_btn.setFixedWidth(200)

                    layout.addWidget(delete_btn)
                    self.setCellWidget(i, j, container)

        self.verticalHeader().setDefaultSectionSize(50)

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setAlternatingRowColors(True)  

    def emit_delete_signal(self, item: str):
        self.delete_signal.emit(item)
    
    def load_style(self):
        with open(r"C:\Users\Vale\gui-example\style\exercises_page.qss", "r") as f:
            self.setStyleSheet(f.read())


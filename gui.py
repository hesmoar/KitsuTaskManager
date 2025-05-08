import sys
import os

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QCheckBox, QRadioButton, QButtonGroup, QFileDialog, QHBoxLayout, QGroupBox, 
    QFrame, QSpacerItem, QSizePolicy, QComboBox, QTextEdit, QInputDialog, QLineEdit, 
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QFormLayout, QGridLayout, 
    QMessageBox, QListWidget
)
from PySide6.QtCore import Qt
from kitsu_auth import connect_to_kitsu, set_env_variables
from kitsu_utils import get_user_projects, get_user_tasks_for_project


class TaskManager(QMainWindow):


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.setGeometry(50, 50, 400, 300)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)

        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(10)

        # Title label
        self.title_label = QLabel("Task Manager", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        #self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(self.title_label)

        # Log in 
        self.title_label = QLabel("Log in to Kitsu", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)

        self.url_name_label = QLabel("Kitsu URL:", self)
        self.url_name_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.url_name_label)

        self.url_name_input = QLineEdit(self)
        self.url_name_input.setPlaceholderText("Enter your Kitsu URL")
        main_layout.addWidget(self.url_name_input)

        self.user_name_label = QLabel("Username:", self)
        self.user_name_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.user_name_label)

        self.user_name_input = QLineEdit(self)
        self.user_name_input.setPlaceholderText("Enter your username")
        main_layout.addWidget(self.user_name_input)

        self.password_label = QLabel("Password:", self)
        self.password_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.password_label)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        main_layout.addWidget(self.password_input)

        self.input_button = QPushButton("Log in", self)
        self.input_button.clicked.connect(self.start_process)
        main_layout.addWidget(self.input_button)

        self.apply_stylesheet()


    def apply_stylesheet(self):
         self.setStyleSheet("""             
            QMainWindow {
                background-color: #2E2E2E;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 16px;
            }
            title_label {
                font-size: 35px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #3E3E3E;
                color: #FFFFFF;
                border: 1px solid #555555;
                padding: 5px;
            }
            QPushButton {
                background-color: #007ACC;
                color: #FFFFFF;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #005FA3;
            }
            """)
         

    def get_selections(self):
        self.selections = {
            "kitsu_url": self.url_name_input.text(),
            "kitsu_username": self.user_name_input.text(),
            "kitsu_password": self.password_input.text(),
        }
        return self.selections
    
    def start_process(self):
        self.get_selections()
        print("Starting process with selections:")
        print(self.selections)
        set_env_variables(
            self.selections["kitsu_url"],
            self.selections["kitsu_username"],
            self.selections["kitsu_password"]
        )
        connect_to_kitsu(
            self.selections["kitsu_url"],
            self.selections["kitsu_username"],
            self.selections["kitsu_password"]
        )
        #self.close()
        self.update_ui_with_kitsu()
    
    def update_ui_with_kitsu(self):
        central_widget = self.centralWidget()
        main_layout = central_widget.layout()

        for i in reversed(range(main_layout.count())):
            widget = main_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        first_level = QHBoxLayout()
        # Left Column
        left_column = QVBoxLayout()

        project_group = QGroupBox("Project")
        project_layout = QVBoxLayout(project_group)


        self.projects_label = QLabel("Kitsu Projects")
        self.projects_label.setAlignment(Qt.AlignCenter)
        project_layout.addWidget(self.projects_label)

        self.projects_list = QListWidget(self)
        self.projects_list.addItems(get_user_projects())
        self.projects_list.itemClicked.connect(self.on_project_selected)
        project_layout.addWidget(self.projects_list)

        left_column.addWidget(project_group)

        # Right Column is for tasks and other info
        right_column = QVBoxLayout()

        entity_group = QGroupBox("Entity")
        entity_layout = QVBoxLayout(entity_group)

        self.entity_label = QLabel("Entity")
        self.entity_label.setAlignment(Qt.AlignCenter)
        entity_layout.addWidget(self.entity_label)

        self.entity_list = QListWidget(self)
        self.entity_list.addItems(["Entities"])
        entity_layout.addWidget(self.entity_list)

        right_column.addWidget(entity_group)



        first_level.addLayout(left_column)
        first_level.addLayout(right_column)

        second_level = QHBoxLayout()

        second_right_column = QVBoxLayout()

        tasks_group = QGroupBox("Tasks")
        tasks_layout = QVBoxLayout(tasks_group)

        self.tasks_label = QLabel("Tasks")
        self.tasks_label.setAlignment(Qt.AlignCenter)
        tasks_layout.addWidget(self.tasks_label)

        self.tasks_list = QListWidget(self)
        self.tasks_list.addItems(["Your tasks"])
        tasks_layout.addWidget(self.tasks_list)

        second_right_column.addWidget(tasks_group)

        second_level.addLayout(second_right_column)



        main_layout.addLayout(first_level)
        main_layout.addLayout(second_level)



    


    def on_project_selected(self, item):
        selected_project = item.text()
        entities, tasks = get_user_tasks_for_project(self.selections["kitsu_username"], selected_project)
        self.entity_list.clear()
        self.tasks_list.clear()

        self.entity_list.addItems(entities)

        self.tasks_list.addItems(tasks)


def run_gui():
    app = QApplication(sys.argv)
    window = TaskManager()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_gui()
import sys
import os

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QCheckBox, QRadioButton, QButtonGroup, QFileDialog, QHBoxLayout, QGroupBox, 
    QFrame, QSpacerItem, QSizePolicy, QComboBox, QTextEdit, QInputDialog, QLineEdit, 
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QFormLayout, QGridLayout, 
    QMessageBox, QListWidget, QListWidgetItem, QMenu
)
from PySide6.QtGui import QIcon, QPixmap, QFont, QColor, QPalette
from PySide6.QtCore import Qt
from kitsu_auth import connect_to_kitsu, set_env_variables, save_credentials
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
            background-color: #1f1f1f;
        }

        QLabel {
            color: #f0f0f0;
            font-size: 14px;
        }

        QGroupBox {
            color: #f0f0f0;
            font-size: 16px;
            font-weight: bold;
            border: 1px solid #444;
            border-radius: 8px;
            margin-top: 10px;
        }

        QGroupBox:title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;
        }

        QLineEdit, QTextEdit {
            background-color: #2c2c2c;
            color: #fff;
            border: 1px solid #555;
            padding: 6px;
            border-radius: 4px;
        }

        QPushButton {
            background-color: #007acc;
            color: #ffffff;
            font-weight: bold;
            border-radius: 5px;
            padding: 8px 12px;
        }

        QPushButton:hover {
            background-color: #005fa3;
        }

        QListWidget {
            background-color: #2a2a2a;
            color: white;
            border: 1px solid #444;
        }

        QListWidget::item:selected {
            background-color: #007acc;
            color: white;
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
        #print(self.selections)
        #set_env_variables(
        #    self.selections["kitsu_url"],
        #    self.selections["kitsu_username"],
        #    self.selections["kitsu_password"]
        #)

        #save_credentials(
        #    self.selections["kitsu_url"],
        #    self.selections["kitsu_username"],
        #    self.selections["kitsu_password"]
        #)

        connect_to_kitsu(
            self.selections["kitsu_url"],
            self.selections["kitsu_username"],
            self.selections["kitsu_password"]
        )
        #self.close()
        self.update_ui_with_kitsu()
    
    def update_ui_with_kitsu(self):

        self.setGeometry(100, 100, 800, 600)

        central_widget = self.centralWidget()
        main_layout = central_widget.layout()

        for i in reversed(range(main_layout.count())):
            widget = main_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        header_level = QHBoxLayout()

        self.header_label = QLabel("Welcome", self)
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_level.addWidget(self.header_label)

        self.username_label = QLabel(self.selections["kitsu_username"], self)
        self.username_label.setAlignment(Qt.AlignCenter)
        self.username_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_level.addWidget(self.username_label)

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
        self.entity_list.itemClicked.connect(self.on_entity_selected)
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



        main_layout.addLayout(header_level)
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addLayout(first_level)
        main_layout.addLayout(second_level)
        
        self.apply_stylesheet()


    def add_task_to_list(self, task_type_name, due_date, status, entity_name):
        # Create a custom widget for the task
        task_widget = QWidget()
        task_layout = QHBoxLayout(task_widget)


        # Add task details (name and date)
        text_layout = QVBoxLayout()
        task_entity_name_label = QLabel(entity_name)
        task_entity_name_label.setStyleSheet("color: black; font-weight: bold;")
        task_name_label = QLabel(task_type_name)
        task_name_label.setStyleSheet("color: black; font-weight: bold;")
        task_date_label = QLabel(due_date)
        task_date_label.setStyleSheet("color: black; font-size: 12px;")
        task_status_label = QLabel(status)
        task_status_label.setStyleSheet("color: black; font-size: 12px;")
        text_layout.addWidget(task_entity_name_label)
        text_layout.addWidget(task_name_label)
        text_layout.addWidget(task_date_label)
        text_layout.addWidget(task_status_label)

        task_layout.addLayout(text_layout)

        # Add the custom widget to the QListWidget
        task_item = QListWidgetItem(self.tasks_list)
        task_item.setSizeHint(task_widget.sizeHint())
        self.tasks_list.addItem(task_item)
        self.tasks_list.setItemWidget(task_item, task_widget)
    


    def on_project_selected(self, item):
        selected_project = item.text()
        entities, self.task_details = get_user_tasks_for_project(self.selections["kitsu_username"], selected_project)
        self.entity_list.clear()
        self.tasks_list.clear()

        self.entity_list.addItems(entities)



    def on_entity_selected(self, item):
        selected_entity = item.text()
        # Do something with the selected entity
        print(f"Selected entity: {selected_entity}")

        filtered_tasks = [
            task for task in self.task_details if task["entity_name"] == selected_entity

        ]

        self.tasks_list.clear()

        for task in filtered_tasks:
            task_name = task["task_type_name"]
            due_date = task["due_date"]
            status = task["status"]
            self.add_task_to_list(task_name, due_date, status, selected_entity)
    
    def contextMenuEvent(self, event):
        if self.tasks_list.underMouse():
            menu = QMenu(self)

            action_view_details = menu.addAction("View Details")

            action = menu.exec_(self.mapToGlobal(event.pos()))

            if action == action_view_details:
                self.view_task_details()
    
    def view_task_details(self):
        selected_items = self.tasks_list.currentItem()
        if selected_items:
            selected_task = selected_items[0].text()
            QMessageBox.information(self, "Task Details", f"Details for task: {selected_task}")




def run_gui():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = TaskManager()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_gui()
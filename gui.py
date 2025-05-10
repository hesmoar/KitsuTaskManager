import sys
import os

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QCheckBox, QRadioButton, QButtonGroup, QFileDialog, QHBoxLayout, QGroupBox, 
    QFrame, QSpacerItem, QSizePolicy, QComboBox, QTextEdit, QInputDialog, QLineEdit, 
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QFormLayout, QGridLayout, 
    QMessageBox, QListWidget, QListWidgetItem, QMenu, QToolButton, QSizeGrip
)
from PySide6.QtGui import QIcon, QPixmap, QFont, QColor, QPalette
from PySide6.QtCore import Qt, QSize
from kitsu_auth import connect_to_kitsu, set_env_variables, save_credentials, load_credentials, clear_credentials
from kitsu_utils import get_user_projects, get_user_tasks_for_project, get_preview_thumbnail, clean_up_thumbnails


class TaskManager(QMainWindow):


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.setGeometry(50, 50, 400, 300)

        stored_credentials = load_credentials()
        if stored_credentials:
            self.selections = stored_credentials
            self.auto_login()
            if self.auto_login():
                return
            
        self.show_login_screen()


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
        
        QToolButton {
            background-color: #2c2c2c;
            color: #f0f0f0;
            border: 1px solid #444;
            padding: 6px;
            border-radius: 4px;
        }
        QToolButton:hover {
            background-color: #007acc;
        }
    """)
         
    def show_login_screen(self):
        """Display the login screen."""
        central_widget = QWidget(self)
        self.setGeometry(50, 50, 400, 300)
        self.setCentralWidget(central_widget)

        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        central_widget.setLayout(main_layout)

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

    def auto_login(self):
        try:
            #print(f"Loaded credentials: {stored_credentials}")
            connect_to_kitsu(
                self.selections["kitsu_url"],
                self.selections["username"],
                self.selections["password"]
            )
            self.update_ui_with_kitsu()
            return True
        except Exception as e:
            QMessageBox.warning(self, "Auto-Login Failed", f"Auto-login failed: {str(e)}")
            return False

    def get_selections(self):
        self.selections = {
            "kitsu_url": self.url_name_input.text(),
            "username": self.user_name_input.text(),
            "password": self.password_input.text(),
        }
        return self.selections
    
    def start_process(self):
        self.get_selections()
        print("Starting process with selections:")

        try:
            connect_to_kitsu(
                self.selections["kitsu_url"],
                self.selections["username"],
                self.selections["password"]
            )

            self.update_ui_with_kitsu()
        except Exception as e:
            QMessageBox.warning(self, "Login Failed", f"Login failed: {str(e)}")


    def logout(self):
        clear_credentials()
        self.selections = {}
        clean_up_thumbnails()
        QMessageBox.information(self, "Logout", "You have been logged out.")
        
        self.setGeometry(50, 50, 400, 300)
        self.show_login_screen()


    def update_ui_with_kitsu(self):

        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        central_widget.setLayout(main_layout)



        for i in reversed(range(main_layout.count())):
            widget = main_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        header_level = QHBoxLayout()

        header_left_column = QVBoxLayout()
        header_left_column.setAlignment(Qt.AlignLeft)



        self.header_label = QLabel("Welcome", self)
        self.header_label.setAlignment(Qt.AlignLeft)
        self.header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_left_column.addWidget(self.header_label)

        header_right_column = QVBoxLayout()
        header_right_column.setAlignment(Qt.AlignRight)


        self.username_button = QToolButton(self)
        self.username_button.setText(self.selections["username"])
        self.username_button.setIcon(QIcon(r"D:\HecberryStuff\Dev\photo.png"))
        self.username_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        menu = QMenu(self)
        menu.addAction("Profile", self.view_profile)
        menu.addAction("Settings", self.view_settings)
        menu.addAction("Logout", self.logout)

        self.username_button.setMenu(menu)
        self.username_button.setPopupMode(QToolButton.InstantPopup)
        header_right_column.addWidget(self.username_button)

        header_level.addLayout(header_left_column)
        header_level.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Expanding))
        header_level.addLayout(header_right_column)
        header_level.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Expanding))

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

    def view_profile(self):
        QMessageBox.information(self, "Profile", "Viewing profile...")
    
    def view_settings(self):
        QMessageBox.information(self, "Settings", "Opening settings...")

    def add_task_to_list(self, task_type_name, due_date, status, entity_name, id):
        # Create a custom widget for the task
        task_widget = QWidget()
        task_layout = QHBoxLayout(task_widget)


        # Add task details (name and date)
        text_layout_right = QVBoxLayout()
        text_layout_left = QVBoxLayout()

        thumbnail_path = get_preview_thumbnail(id)
        task_preview_icon_button = QToolButton(self)
        if thumbnail_path:
            pixmap = QPixmap(thumbnail_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            task_preview_icon_button.setIcon(QIcon(pixmap))
        else:
            task_preview_icon_button.setIcon(QIcon(r"D:\HecberryStuff\Dev\photo.png"))
        
        task_preview_icon_button.setIconSize(QSize(100, 100))
        task_preview_icon_button.setFixedSize(100, 100)

        task_entity_name_label = QLabel(entity_name)
        task_entity_name_label.setStyleSheet("font-weight: bold;")
        task_name_label = QLabel(task_type_name)
        task_name_label.setStyleSheet("font-weight: bold;")
        task_date_label = QLabel(due_date)
        task_date_label.setStyleSheet("font-size: 12px;")
        task_status_label = QLabel(status)
        task_status_label.setStyleSheet("font-size: 12px;")
        text_layout_left.addWidget(task_preview_icon_button)
        text_layout_right.addWidget(task_entity_name_label)
        text_layout_right.addWidget(task_name_label)
        text_layout_right.addWidget(task_date_label)
        text_layout_right.addWidget(task_status_label)

        task_layout.addLayout(text_layout_left)
        task_layout.addLayout(text_layout_right)

        # Add the custom widget to the QListWidget
        task_item = QListWidgetItem(self.tasks_list)
        task_item.setSizeHint(task_widget.sizeHint())
        self.tasks_list.addItem(task_item)
        self.tasks_list.setItemWidget(task_item, task_widget)
    


    def on_project_selected(self, item):
        selected_project = item.text()
        entities, self.task_details = get_user_tasks_for_project(self.selections["username"], selected_project)
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
            id = task["task_id"]
            self.add_task_to_list(task_name, due_date, status, selected_entity, id)
    
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
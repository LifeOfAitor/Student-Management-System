from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QGridLayout, QLabel, QWidget, \
    QLineEdit, QPushButton, QComboBox, QMainWindow, QTableWidget
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        # create main menu
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        # create submenus
        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # create table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "NAME", "COURSE", "MOBILE"))
        self.setCentralWidget(self.table)

    def load_data(self):
        self.table


# display app
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())

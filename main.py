from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QGridLayout, QLabel, QWidget, \
    QLineEdit, QPushButton, QComboBox, QMainWindow, QTableWidget, \
    QTableWidgetItem, QDialog, QVBoxLayout
import sys
import sqlite3


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(500)

        layout = QVBoxLayout()

        # create widgets



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        # create main menu
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        # create submenus
        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # create table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "NAME", "COURSE", "MOBILE"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    # populate table with database data
    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        # loop for every row and then every row item
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number,
                                   QTableWidgetItem(str(data)))
        connection.close()

    # generates an Insert Dialog that will display a new dialog to add the data
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

# display app
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())

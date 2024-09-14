import sqlite3
import sys
from pyexpat.errors import messages

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QGridLayout, QLabel, QLineEdit, \
    QPushButton, QComboBox, QMainWindow, QTableWidget, \
    QTableWidgetItem, QDialog, QVBoxLayout, QToolBar, QStatusBar, QMessageBox


class DatabaseConnection:
    def __init__(self, database_name="database.db"):
        self.database_name = database_name

    def connect(self):
        connection = sqlite3.connect(self.database_name)
        return connection


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        content = """
        This app is a simple app to learn how to manage data from a small
        database and learn how to implement a basic GUI to work with the data.
        """
        self.setWindowTitle("About")
        self.setText(content)


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(200)

        layout = QVBoxLayout()

        # create widgets
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        self.phone_number = QLineEdit()
        self.phone_number.setPlaceholderText("123456789")
        layout.addWidget(self.phone_number)

        button = QPushButton("Add Student")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.phone_number.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) "
                       "values(?, ?, ?)", (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        self.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(150)

        layout = QVBoxLayout()

        # create widgets
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        button = QPushButton("Search")
        button.clicked.connect(self.search_student)
        layout.addWidget(button)

        # if necessary show message
        self.output_text = QLabel()
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def search_student(self):
        name = self.student_name.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = (?)",
                                (name,))
        rows = list(result)
        if len(rows) < 1:
            self.output_text.setText(f"Student with name {name} not found")
        else:
            self.output_text.setText("")
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)
        cursor.close()
        connection.close()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(200)

        layout = QVBoxLayout()

        # load selected student data to visualize the name by default
        index = main_window.table.currentRow()
        selected_student_name = main_window.table.item(index, 1).text()
        selected_student_course = main_window.table.item(index, 2).text()
        selected_student_phone = main_window.table.item(index, 3).text()
        self.selected_student_id = main_window.table.item(index, 0).text()
        # create widgets
        self.student_name = QLineEdit(selected_student_name)
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(selected_student_course)
        layout.addWidget(self.course_name)

        self.phone_number = QLineEdit(selected_student_phone)
        layout.addWidget(self.phone_number)

        button = QPushButton("Update Student")
        button.clicked.connect(self.edit_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def edit_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.phone_number.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, "
                       "mobile = ? WHERE id = ?",
                       (name, course, mobile, self.selected_student_id))
        connection.commit()
        cursor.close()
        connection.close()
        self.close()
        main_window.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout()

        # get name from table
        index = main_window.table.currentRow()
        self.selected_student_name = main_window.table.item(index, 1).text()

        # create widgets
        delete_prompt = QLabel(
            f"Delete data from {self.selected_student_name}?")
        yes_button = QPushButton("YES")
        no_button = QPushButton("NO")

        # add widgets to grid
        layout.addWidget(delete_prompt, 0, 0, 1, 2)
        layout.addWidget(yes_button, 1, 0)
        layout.addWidget(no_button, 1, 1)

        # add functionality to buttons
        yes_button.clicked.connect(self.delete_student)

        self.setLayout(layout)

    def delete_student(self):
        name = self.selected_student_name
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE name = ?", (name,))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()

        # create a confirmation message
        confirmation = QMessageBox()
        confirmation.setText(f"{name} was deleted")
        confirmation.exec()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(400, 400)

        # create main menu
        file_menu_item = self.menuBar().addMenu("&File")
        search_menu_item = self.menuBar().addMenu("&Edit")
        help_menu_item = self.menuBar().addMenu("&Help")

        # create submenus and add actions to them
        # create action (ICON, TEXT, self)
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student",
                                     self)
        # what to do when the action is triggered
        add_student_action.triggered.connect(self.insert)
        # add action to menu item
        file_menu_item.addAction(add_student_action)

        search_menu_action = QAction(QIcon("icons/search.png"),
                                     "Search Student", self)
        search_menu_action.triggered.connect(self.search)
        search_menu_item.addAction(search_menu_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # create table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "NAME", "COURSE", "MOBILE"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # create toolbar and add it to the main window
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        # add actions to the toolbar items
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_menu_action)

        # create and add status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # detect what cell is selected to trigger actions like edit or delete
        self.table.cellClicked.connect(self.cell_clicked)

    # when a cell is selected the edit and delete buttons appear
    def cell_clicked(self):
        edit_button = QPushButton("Edit Student")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Student")
        delete_button.clicked.connect(self.delete)

        # only add buttons if there are not, otherwise it would create the
        # buttons whenever a cell is selected
        children = self.findChildren(QPushButton)
        if not children:
            self.status_bar.addWidget(edit_button)
            self.status_bar.addWidget(delete_button)

    # populate table with database data
    def load_data(self):
        connection = DatabaseConnection().connect()
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        # loop for every row and then every row item
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number,
                                   QTableWidgetItem(str(data)))
        connection.close()

    # generates an Insert Dialog to add the data
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    # generates a search dialog to search for students
    def search(self):
        search_dialog = SearchDialog()
        search_dialog.exec()

    def about(self):
        about_dialog = AboutDialog()
        about_dialog.exec()

    # generates a edit dialog to edit selected student data
    def edit(self):
        edit_dialog = EditDialog()
        edit_dialog.exec()

    # generates a delete dialog to delete selected student
    def delete(self):
        delete_dialog = DeleteDialog()
        delete_dialog.exec()


# display app
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())

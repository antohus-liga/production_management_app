from PySide6.QtWidgets import QMainWindow, QStackedWidget

from ui.main_menu import MainMenu
from ui.tables.clients import ClientsTable


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Manager")

        self.stack = QStackedWidget()

        self.main_menu = MainMenu(self.stack)
        self.clients_table = ClientsTable(self.stack)

        self.stack.addWidget(self.main_menu)
        self.stack.addWidget(self.clients_table)

        self.setCentralWidget(self.stack)

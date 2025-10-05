from PySide6.QtWidgets import QMainWindow, QStackedWidget

from ui.main_menu import MainMenu
from ui.tables.client_widget import ClientWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Production Manager")

        self.stack = QStackedWidget()

        self.main_menu = MainMenu(self.stack)
        self.client_table = ClientWidget(self.stack)

        self.stack.addWidget(self.main_menu)
        self.stack.addWidget(self.client_table)

        self.setCentralWidget(self.stack)

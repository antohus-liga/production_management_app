from PySide6.QtWidgets import QMainWindow, QStackedWidget

from sql.db_manager import create_connection
from ui.main_menu import MainMenu
from ui.tables.client_widget import ClientWidget
from ui.tables.supplier_widget import SupplierWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        db = create_connection()
        self.setWindowTitle("Production Manager")

        self.stack = QStackedWidget()

        self.main_menu = MainMenu(self.stack)
        self.client_table = ClientWidget(self.stack, db)
        self.suppliers_table = SupplierWidget(self.stack, db)

        self.stack.addWidget(self.main_menu)
        self.stack.addWidget(self.client_table)
        self.stack.addWidget(self.suppliers_table)

        self.setCentralWidget(self.stack)

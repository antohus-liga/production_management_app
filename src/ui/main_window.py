from PySide6.QtWidgets import QMainWindow, QStackedWidget

from sql.db_manager import create_connection
from ui.main_menu import MainMenu
from ui.tables.client_widget import ClientWidget
from ui.tables.material_widget import MaterialWidget
from ui.tables.product_widget import ProductWidget
from ui.tables.production_widget import ProductionWidget
from ui.tables.supplier_widget import SupplierWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        db = create_connection()
        self.setWindowTitle("Production Manager")

        self.stack = QStackedWidget()

        widgets = (
            MainMenu(self.stack),
            ClientWidget(self.stack, db),
            SupplierWidget(self.stack, db),
            MaterialWidget(self.stack, db),
            ProductWidget(self.stack, db),
            ProductionWidget(self.stack, db),
        )

        for w in widgets:
            self.stack.addWidget(w)

        production_widget = next(w for w in widgets if isinstance(w, ProductionWidget))
        product_widget = next(w for w in widgets if isinstance(w, ProductWidget))

        production_widget.quantity_updated.connect(
            lambda: product_widget.table_widget.table_view.model.select()
        )

        self.setCentralWidget(self.stack)

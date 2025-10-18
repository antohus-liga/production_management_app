from PySide6.QtCore import QSize, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QTabWidget

from sql.db_manager import create_connection
from ui.main_menu import MainMenu
from ui.tables.client_widget import ClientWidget
from ui.tables.material_widget import MaterialWidget
from ui.tables.movements_in_widget import MovementsInWidget
from ui.tables.movements_out_widget import MovementsOutWidget
from ui.tables.product_widget import ProductWidget
from ui.tables.production_widget import ProductionWidget
from ui.tables.supplier_widget import SupplierWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        db = create_connection()
        self.setWindowTitle("Production Manager")

        tabs = QTabWidget()
        self._welcome_shown = True

        # Instantiate widgets once so we can connect signals across tabs
        welcome_widget = MainMenu(tabs)
        self.client_widget = ClientWidget(tabs, db)
        self.supplier_widget = SupplierWidget(tabs, db)
        self.material_widget = MaterialWidget(tabs, db)
        self.movements_in_widget = MovementsInWidget(tabs, db)
        self.movements_out_widget = MovementsOutWidget(tabs, db)
        self.product_widget = ProductWidget(tabs, db)
        self.production_widget = ProductionWidget(tabs, db)

        # Add tabs with icons
        tabs.addTab(welcome_widget, QIcon(":/icons/production.png"), "Welcome")
        tabs.addTab(
            self.client_widget, QIcon(":/icons/customer-service.png"), "Clients"
        )
        tabs.addTab(self.supplier_widget, QIcon(":/icons/supplier.png"), "Suppliers")
        tabs.addTab(
            self.material_widget, QIcon(":/icons/raw-material.png"), "Materials"
        )
        tabs.addTab(
            self.movements_in_widget, QIcon(":/icons/delivery.png"), "Movements In"
        )
        tabs.addTab(
            self.movements_out_widget, QIcon(":/icons/sale.png"), "Movements Out"
        )
        tabs.addTab(self.product_widget, QIcon(":/icons/product.png"), "Products")
        tabs.addTab(
            self.production_widget, QIcon(":/icons/production.png"), "Production"
        )

        # Optional: unify icon sizes similar to the old menu
        tabs.setIconSize(QSize(24, 24))

        # When production changes, refresh product table model
        self.production_widget.quantity_updated.connect(self._update_quantities)
        self.movements_out_widget.values_updated.connect(self._update_quantities)
        self.movements_in_widget.values_updated.connect(self._update_quantities)

        # Remove welcome tab after first switch to any table tab
        def handle_tab_change(index: int):
            if self._welcome_shown and index > 0:
                tabs.blockSignals(True)
                # Preserve the intended tab after removing index 0
                intended = index - 1
                tabs.removeTab(0)
                self._welcome_shown = False
                tabs.setCurrentIndex(intended)
                tabs.blockSignals(False)

        tabs.currentChanged.connect(handle_tab_change)

        self.setCentralWidget(tabs)

    def _update_quantities(self):
        self.product_widget.master.table_view.model.select()
        self.material_widget.table_widget.table_view.model.select()
        QTimer.singleShot(
            0, self.movements_in_widget.table_widget.table_view.model.select
        )
        QTimer.singleShot(
            0, self.movements_out_widget.table_widget.table_view.model.select
        )

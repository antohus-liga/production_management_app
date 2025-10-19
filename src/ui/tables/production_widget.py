from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from sql.db_manager import recalc_all_quantities
from ui.tables.components.table_widget import TableWidget


class ProductionWidget(QWidget):
    quantity_updated = Signal()

    def __init__(self, stack, db):
        super().__init__()
        self.stack = stack

        self.table_widget = TableWidget(
            self.stack, "production", db, "Produção")
        self.table_widget.table_view.model.dataChanged.connect(
            self.trigger_product_update
        )

        self.setLayout(self.table_widget.layout)

    def trigger_product_update(self):
        recalc_all_quantities()
        self.quantity_updated.emit()

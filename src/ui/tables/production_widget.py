from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from sql.db_manager import recalc_product_quantities
from ui.tables.components.table_widget import TableWidget


class ProductionWidget(QWidget):
    quantity_updated = Signal()

    def __init__(self, stack, db):
        super().__init__()
        self.stack = stack

        self.table_widget = TableWidget(self.stack, "production", db)
        self.table_widget.confirm_btn.clicked.connect(self.submit_changes)

        self.setLayout(self.table_widget.layout)

    def submit_changes(self) -> None:
        self.table_widget.table_view.model.submitAll()
        self.table_widget.table_view.delegate.new_rows.clear()
        self.table_widget.table_view.delegate.deleted_rows.clear()

        recalc_product_quantities()

        self.quantity_updated.emit()

        self.table_widget.table_view.viewport().update()

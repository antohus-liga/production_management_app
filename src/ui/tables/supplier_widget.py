from PySide6.QtWidgets import QWidget

from ui.tables.components.table_widget import TableWidget


class SupplierWidget(QWidget):
    def __init__(self, stack, db):
        super().__init__()
        self.stack = stack
        self.table_widget = TableWidget(self.stack, "suppliers", db)

        self.setLayout(self.table_widget.layout)

from PySide6.QtWidgets import QWidget

from ui.tables.components.product_table_widget import ProductTableWidget


class ProductWidget(QWidget):
    def __init__(self, stack, db):
        super().__init__()
        self.stack = stack
        self.table_widget = ProductTableWidget(self.stack, db)

        self.setLayout(self.table_widget.layout)

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QVBoxLayout, QWidget

import ui.resources.resources_rc
from ui.tables.components.subcomponents.push_button import PushButton
from ui.tables.components.table_widget import TableWidget


class SupplierWidget(QWidget):
    def __init__(self, stack, db):
        super().__init__()
        self.stack = stack

        self.table_widget = TableWidget(self.stack, "suppliers", db)

        self.widget_layout = QVBoxLayout()
        self.widget_layout.addWidget(self.table_widget)

        self.setLayout(self.widget_layout)

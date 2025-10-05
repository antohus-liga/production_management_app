from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QVBoxLayout, QWidget

import ui.resources.resources_rc
from ui.tables.components.subcomponents.push_button import PushButton
from ui.tables.components.table_widget import TableWidget


class ClientWidget(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.table_widget = TableWidget("clients")

        go_back_btn = PushButton("Go back")
        go_back_btn.setIcon(QIcon(":/icons/back-arrow.png"))
        go_back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        self.widget_layout = QVBoxLayout()
        self.widget_layout.addWidget(go_back_btn)
        self.widget_layout.addWidget(self.table_widget)

        self.setLayout(self.widget_layout)

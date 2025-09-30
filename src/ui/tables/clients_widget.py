from PySide6.QtWidgets import (QHeaderView, QPushButton, QSizePolicy,
                               QTableView, QVBoxLayout, QWidget)

from ui.tables.clients_model import ClientsTableModel


class ClientsWidget(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.model = ClientsTableModel(self)

        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        self.table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.table_view.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

        go_back_btn = QPushButton("Go back")
        go_back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        layout = QVBoxLayout()

        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size.setHorizontalStretch(1)
        self.table_view.setSizePolicy(size)

        layout.addWidget(self.table_view)
        layout.addWidget(go_back_btn)

        self.setLayout(layout)

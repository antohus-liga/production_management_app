from PySide6.QtWidgets import (QHBoxLayout, QHeaderView, QPushButton,
                               QSizePolicy, QTableView, QVBoxLayout, QWidget)

from ui.tables.clients_model import TableModel


class ClientsWidget(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.model = TableModel(self)

        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        self.table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.table_view.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.table_view.setSelectionBehavior(QTableView.SelectRows)

        go_back_btn = QPushButton("Go back")
        go_back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size.setHorizontalStretch(1)
        self.table_view.setSizePolicy(size)
        self.table_view.verticalHeader().setVisible(False)

        confirm_btn = QPushButton("confirm changes")
        add_btn = QPushButton("insert")
        delete_btn = QPushButton("delete")
        refresh_btn = QPushButton("refresh")

        add_btn.clicked.connect(
            lambda: self.model.insertRow(self.model.rowCount()))
        confirm_btn.clicked.connect(lambda: self.model.submitAll())
        delete_btn.clicked.connect(self.delete_selected)
        refresh_btn.clicked.connect(self.model.select)

        util_layout = QHBoxLayout()
        util_layout.addWidget(add_btn)
        util_layout.addWidget(confirm_btn)
        util_layout.addWidget(delete_btn)
        util_layout.addWidget(refresh_btn)

        layout = QVBoxLayout()
        layout.addWidget(go_back_btn)
        layout.addWidget(self.table_view)
        layout.addLayout(util_layout)

        self.setLayout(layout)

    def delete_selected(self) -> None:
        selection = self.table_view.selectionModel().selectedRows()
        for index in selection:
            self.model.removeRow(index.row())

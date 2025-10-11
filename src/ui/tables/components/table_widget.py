import uuid

from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout,
                               QWidget)

import ui.resources.resources_rc
from ui.tables.components.subcomponents.push_button import PushButton
from ui.tables.components.subcomponents.table_view import TableView


class TableWidget(QWidget):
    def __init__(self, stack, table, db):
        super().__init__()
        self.table = table
        self.stack = stack
        self.font = QFont()
        self.font.setPointSize(24)

        self.table_view = TableView(self.table, db)

        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size.setHorizontalStretch(1)
        self.table_view.setSizePolicy(size)
        self.table_view.verticalHeader().setVisible(False)

        table_label = QLabel(self.table.capitalize())
        table_label.setFixedHeight(30)
        table_label.setFont(self.font)

        go_back_btn = PushButton("Go back")
        go_back_btn.setIcon(QIcon(":/icons/back-arrow.png"))
        add_btn = PushButton("Insert New Row")
        add_btn.setIcon(QIcon(":/icons/plus.png"))
        delete_btn = PushButton("Delete Selected")
        delete_btn.setIcon(QIcon(":/icons/bin.png"))

        go_back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        add_btn.clicked.connect(self.insert_row)
        delete_btn.clicked.connect(self.delete_selected)

        util_layout = QHBoxLayout()
        util_layout.addWidget(add_btn)
        util_layout.addWidget(delete_btn)

        self.layout = QVBoxLayout()
        self.layout.addWidget(table_label)
        self.layout.addWidget(go_back_btn)
        self.layout.addWidget(self.table_view)
        self.layout.addLayout(util_layout)

        self.setLayout(self.layout)

    def delete_selected(self) -> None:
        selection = self.table_view.selectionModel().selectedRows()
        if not selection:
            return

        for index in sorted(selection, key=lambda x: x.row(), reverse=True):
            row = index.row()
            self.table_view.model.removeRow(row)

        if not self.table_view.model.submitAll():
            print("Delete failed:", self.table_view.model.lastError().text())
            self.table_view.model.revertAll()
        else:
            self.table_view.model.select()

    def insert_row(self):
        row = self.table_view.model.rowCount()
        self.table_view.model.insertRow(row)

        if self.table != "production":
            new_code = f"{self.table[:3:].upper()}{uuid.uuid4().hex[:8]}"
            self.table_view.model.setData(
                self.table_view.model.index(row, 0), new_code)

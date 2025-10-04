from PySide6.QtWidgets import (QHBoxLayout, QHeaderView, QPushButton,
                               QSizePolicy, QTableView, QVBoxLayout, QWidget)

from ui.tables.sql_table_model import TableModel
from ui.tables.unsubmitted_highlight import HighlightDelegate


class ClientsWidget(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.model = TableModel(self, "clients")

        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        self.delegate = HighlightDelegate(self.table_view)
        self.table_view.setItemDelegate(self.delegate)

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
        discard_btn = QPushButton("discard changes")

        add_btn.clicked.connect(self.insert_row)
        delete_btn.clicked.connect(self.delete_selected)
        discard_btn.clicked.connect(self.discard_changes)
        confirm_btn.clicked.connect(self.submit_changes)

        util_layout = QHBoxLayout()
        util_layout.addWidget(add_btn)
        util_layout.addWidget(delete_btn)
        util_layout.addWidget(discard_btn)
        util_layout.addWidget(confirm_btn)

        layout = QVBoxLayout()
        layout.addWidget(go_back_btn)
        layout.addWidget(self.table_view)
        layout.addLayout(util_layout)

        self.setLayout(layout)

    def delete_selected(self) -> None:
        selection = self.table_view.selectionModel().selectedRows()
        if not selection:
            return

        for index in sorted(selection, key=lambda x: x.row(), reverse=True):
            row = index.row()
            self.model.removeRow(row)

            if row in self.delegate.new_rows:
                self.delegate.new_rows.remove(row)

            self.delegate.deleted_rows.add(row)
            self.table_view.viewport().update()

    def insert_row(self) -> None:
        row = self.model.rowCount()
        self.model.insertRow(row)

        if row in self.delegate.deleted_rows:
            self.delegate.deleted_rows.remove(row)

        self.delegate.new_rows.add(row)
        self.table_view.viewport().update()

    def discard_changes(self) -> None:
        self.model.revertAll()
        self.delegate.new_rows.clear()
        self.delegate.deleted_rows.clear()
        self.table_view.viewport().update()

    def submit_changes(self) -> None:
        self.model.submitAll()
        self.delegate.new_rows.clear()
        self.delegate.deleted_rows.clear()
        self.table_view.viewport().update()

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QSizePolicy, QVBoxLayout, QWidget

import ui.resources.resources_rc
from ui.tables.components.subcomponents.push_button import PushButton
from ui.tables.components.subcomponents.table_view import TableView


class TableWidget(QWidget):
    def __init__(self, stack, table, db):
        super().__init__()
        self.stack = stack

        self.table_view = TableView(table, db)

        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size.setHorizontalStretch(1)
        self.table_view.setSizePolicy(size)
        self.table_view.verticalHeader().setVisible(False)

        go_back_btn = PushButton("Go back")
        go_back_btn.setIcon(QIcon(":/icons/back-arrow.png"))
        confirm_btn = PushButton("Confirm Changes")
        confirm_btn.setIcon(QIcon(":/icons/right.png"))
        add_btn = PushButton("Insert New Row")
        add_btn.setIcon(QIcon(":/icons/plus.png"))
        delete_btn = PushButton("Delete Selected")
        delete_btn.setIcon(QIcon(":/icons/bin.png"))
        discard_btn = PushButton("Discard Changes")
        discard_btn.setIcon(QIcon(":/icons/undo.png"))

        go_back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        add_btn.clicked.connect(self.insert_row)
        delete_btn.clicked.connect(self.delete_selected)
        discard_btn.clicked.connect(self.discard_changes)
        confirm_btn.clicked.connect(self.submit_changes)

        util_layout = QHBoxLayout()
        util_layout.addWidget(add_btn)
        util_layout.addWidget(delete_btn)
        util_layout.addWidget(discard_btn)
        util_layout.addWidget(confirm_btn)

        self.layout = QVBoxLayout()
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

            if row in self.table_view.delegate.new_rows:
                self.table_view.delegate.new_rows.remove(row)

            self.table_view.delegate.deleted_rows.add(row)
            self.table_view.viewport().update()

    def insert_row(self) -> None:
        row = self.table_view.model.rowCount()
        self.table_view.model.insertRow(row)

        if row in self.table_view.delegate.deleted_rows:
            self.table_view.delegate.deleted_rows.remove(row)

        self.table_view.delegate.new_rows.add(row)
        self.table_view.viewport().update()

    def discard_changes(self) -> None:
        self.table_view.model.revertAll()
        self.table_view.delegate.new_rows.clear()
        self.table_view.delegate.deleted_rows.clear()
        self.table_view.viewport().update()

    def submit_changes(self) -> None:
        self.table_view.model.submitAll()
        self.table_view.delegate.new_rows.clear()
        self.table_view.delegate.deleted_rows.clear()
        self.table_view.viewport().update()

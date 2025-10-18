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

        add_btn = PushButton("Insert New Row")
        add_btn.setIcon(QIcon(":/icons/plus.png"))
        delete_btn = PushButton("Delete Selected")
        delete_btn.setIcon(QIcon(":/icons/bin.png"))
        delete_all_btn = PushButton("Delete All")
        delete_all_btn.setIcon(QIcon(":/icons/bin.png"))

        add_btn.clicked.connect(self.insert_row)
        delete_btn.clicked.connect(self.delete_selected)
        delete_all_btn.clicked.connect(self.delete_all)

        util_layout = QHBoxLayout()
        util_layout.addWidget(delete_all_btn)
        util_layout.addWidget(add_btn)
        util_layout.addWidget(delete_btn)

        self.layout = QVBoxLayout()
        self.layout.addWidget(table_label)
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

        if self.table in ("production", "movements_in", "movements_out"):
            # Auto-increment: get the maximum integer key and increment
            new_code = self._get_next_auto_increment()
            self.table_view.model.setData(self.table_view.model.index(row, 0), new_code)
        else:
            # UUID-based key generation
            new_code = f"{self.table[:3].upper()}{uuid.uuid4().hex[:8]}"
            self.table_view.model.setData(self.table_view.model.index(row, 0), new_code)

        # Try to persist the inserted row; if required fields are missing, keep the row pending
        if not self.table_view.model.submitAll():
            print("Insert submit failed:", self.table_view.model.lastError().text())
        else:
            self.table_view.model.select()

    def _get_next_auto_increment(self):
        """
        Get the next auto-increment value by finding the maximum integer key
        in the first column and incrementing it by 1.
        """
        try:
            model = self.table_view.model
            max_value = 0

            # Iterate through all rows to find the maximum integer value
            for row in range(model.rowCount()):
                cell_value = model.data(model.index(row, 0))

                # Handle None or empty values
                if cell_value is None or cell_value == "":
                    continue

                try:
                    # Try to convert to integer
                    int_value = int(cell_value)
                    max_value = max(max_value, int_value)
                except (ValueError, TypeError):
                    # Skip non-integer values
                    continue

            return max_value + 1

        except Exception as e:
            print(f"Error getting next auto-increment value: {e}")
            # Fallback: return 1 if something goes wrong
            return 1

    def delete_all(self) -> None:
        # Efficiently delete all rows from the current table
        db = self.table_view.model.database()
        query = db.exec(f"DELETE FROM {self.table}")
        if query.lastError().isValid():
            print("Delete all failed:", query.lastError().text())
        self.table_view.model.select()

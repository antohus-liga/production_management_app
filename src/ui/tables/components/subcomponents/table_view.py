from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHeaderView, QTableView

from ui.tables.components.subcomponents.length_limit_delegate import \
    LengthLimitedDelegate
from ui.tables.components.subcomponents.sql_table_model import TableModel


class TableView(QTableView):
    def __init__(self, table, db):
        super().__init__()
        self.table = table

        self.model = TableModel(self, self.table, db)
        self.setModel(self.model)
        for i, data in enumerate(self.get_fields_info(self.table)):
            self.model.setHeaderData(i, Qt.Horizontal, data)

        self.delegate = LengthLimitedDelegate(
            self.get_fields_info(self.table), self)
        self.setItemDelegate(self.delegate)

        self.font = QFont()
        self.font.setPointSize(14)

        self.setFont(self.font)
        self.setEditTriggers(QTableView.DoubleClicked |
                             QTableView.SelectedClicked)
        self.setStyleSheet(
            "QLineEdit { background: palette(base); color: palette(text); }"
        )

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setSelectionBehavior(QTableView.SelectRows)

    def get_fields_info(self, table) -> list[dict[str, int]]:
        # TABLE_NAME {FIELD_NAME: CHARACTER_LIMIT}
        # LENGTH = 0: READ-ONLY
        map = {
            "clients": {
                "Code": 15,
                "Name": 60,
                "City": 40,
                "Country": 30,
                "Phone number": 9,
                "Email": 40,
            },
            "suppliers": {
                "Code": 15,
                "Name": 60,
                "City": 40,
                "Country": 30,
                "Phone number": 9,
                "Email": 40,
            },
            "materials": {
                "ID": 15,
                "Description": 80,
                "Quantity": 8,
                "Price p/ Unit": 12,
            },
            "production": {
                "Number": 0,
                "Product": 15,
                "Quantity": 8,
            },
            "products": {
                "ID": 15,
                "Material": 15,
                "Description": 80,
                "Quantity": 0,
                "Selling Price": 12,
            },
        }
        return map[table]

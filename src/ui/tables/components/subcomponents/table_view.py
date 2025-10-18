from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtWidgets import QHeaderView, QTableView

from ui.tables.components.subcomponents.length_limit_delegate import \
    LengthLimitedDelegate
from ui.tables.components.subcomponents.material_combo_delegate import \
    MaterialComboDelegate
from ui.tables.components.subcomponents.sql_table_model import TableModel


class TableView(QTableView):
    def __init__(self, table, db):
        super().__init__()
        self.table = table

        self.model = TableModel(self, self.table, db)
        self.setModel(self.model)
        self.setSortingEnabled(True)
        for i, data in enumerate(self.get_fields_info(self.table)):
            self.model.setHeaderData(i, Qt.Horizontal, data)

        self.delegate = LengthLimitedDelegate(self.get_fields_info(self.table), self)
        self.setItemDelegate(self.delegate)

        # If this is the product_materials detail table, set a combobox delegate for material_id (column 1)
        if self.table == "product_materials":
            self.setItemDelegateForColumn(
                1, MaterialComboDelegate(self.model.database(), self)
            )

        self.font = QFont()
        self.font.setPointSize(14)

        self.setFont(self.font)
        self.setEditTriggers(QTableView.DoubleClicked | QTableView.SelectedClicked)
        self.setStyleSheet(
            "QLineEdit { background: palette(base); color: palette(text); }"
        )

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setSelectionBehavior(QTableView.SelectRows)

        # Expand material_id column for product_materials to fit 15 characters
        if self.table == "product_materials":
            # Column 1 is material_id in product_materials
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
            fm = QFontMetrics(self.font)
            width_px = fm.horizontalAdvance("M" * 15) + 24  # padding for cell margins
            self.setColumnWidth(1, width_px)

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
                "Quantity": 0,
                "Price p/ Unit": 12,
            },
            "production": {
                "Number": 0,
                "Product": 15,
                "Quantity": 8,
                "Created at": 0,
            },
            "products": {
                "ID": 15,
                "Description": 80,
                "Quantity": 0,
                "Selling Price": 12,
            },
            "product_materials": {
                "Product": 0,  # hidden in detail view
                "Material": 15,
                "Qty per unit": 12,
            },
            "movements_in": {
                "Number": 0,
                "Material": 15,
                "Quantity": 8,
                "Total Price": 0,
                "Supplier": 15,
                "Created": 0,
            },
            "movements_out": {
                "Number": 0,
                "Product": 15,
                "Quantity": 8,
                "Total Price": 0,
                "Client": 15,
                "Created": 0,
            },
        }
        return map[table]

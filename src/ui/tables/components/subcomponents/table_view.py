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

        self.delegate = LengthLimitedDelegate(
            self.get_fields_info(self.table), self)
        self.setItemDelegate(self.delegate)

        # If this is the product_materials detail table, set a combobox delegate for material_id (column 1)
        if self.table == "product_materials":
            self.setItemDelegateForColumn(
                1, MaterialComboDelegate(self.model.database(), self)
            )

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

        # Expand material_id column for product_materials to fit 15 characters
        if self.table == "product_materials":
            # Column 1 is material_id in product_materials
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
            fm = QFontMetrics(self.font)
            width_px = fm.horizontalAdvance(
                "M" * 15) + 24  # padding for cell margins
            self.setColumnWidth(1, width_px)

    def get_fields_info(self, table) -> list[dict[str, int]]:
        # TABLE_NAME {FIELD_NAME: CHARACTER_LIMIT}
        # LENGTH = 0: READ-ONLY
        map = {
            "clients": {
                "Código": 15,
                "Nome": 60,
                "Cidade": 40,
                "País": 30,
                "Telemóvel": 9,
                "Email": 40,
            },
            "suppliers": {
                "Código": 15,
                "Nome": 60,
                "Cidade": 40,
                "País": 30,
                "Telemóvel": 9,
                "Email": 40,
            },
            "materials": {
                "ID": 15,
                "Descrição": 80,
                "Quantidade": 0,
                "Preço p/ unidade": 12,
            },
            "production": {
                "Número": 0,
                "Produto": 15,
                "Quantidade": 8,
                "Criado em": 0,
            },
            "products": {
                "ID": 15,
                "Descrição": 80,
                "Quantidade": 0,
                "Preço de venda": 12,
            },
            "product_materials": {
                "Produto": 0,  # hidden in detail view
                "Material": 15,
                "Qtd por unidade": 12,
            },
            "movements_in": {
                "Número": 0,
                "Material": 15,
                "Quantidade": 8,
                "Preço total": 0,
                "Fornecedor": 15,
                "Criado em": 0,
            },
            "movements_out": {
                "Número": 0,
                "Produto": 15,
                "Quantidade": 8,
                "Preço total": 0,
                "Cliente": 15,
                "Criado em": 0,
            },
        }
        return map[table]

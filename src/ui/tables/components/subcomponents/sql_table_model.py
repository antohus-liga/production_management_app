from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlTableModel


class TableModel(QSqlTableModel):
    def __init__(self, parent, table, db):
        super().__init__(parent, db)

        self.setTable(table)
        self.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.select()
        for i, data in enumerate(self.get_header_names(table)):
            self.setHeaderData(i, Qt.Horizontal, data)

    def get_header_names(self, table) -> list[str]:
        map = {
            "clients": ["Code", "Name", "City", "Country", "Phone number", "Email"],
            "suppliers": ["Code", "Name", "City", "Country", "Phone number", "Email"],
            "materials": ["ID", "Description", "Quantity", "Price p/ Unit"],
            "production": ["Number", "Product", "Quantity"],
        }

        return map[table]

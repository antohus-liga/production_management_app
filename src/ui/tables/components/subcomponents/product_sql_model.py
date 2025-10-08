from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlTableModel


class ProductModel(QSqlTableModel):
    def __init__(self, parent, db):
        super().__init__(parent, db)

        self.setTable("products")
        self.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.dataChanged.connect(lambda: self.submitAll())
        self.select()

        for i, data in enumerate(
            ["ID", "Material", "Description", "Quantity", "Selling Price"]
        ):
            self.setHeaderData(i, Qt.Horizontal, data)

    def flags(self, index):
        flags = super().flags(index)
        if index.column() == 3:
            return flags & ~Qt.ItemIsEditable
        return flags

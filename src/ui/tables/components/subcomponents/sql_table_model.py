from PySide6.QtSql import QSqlTableModel


class TableModel(QSqlTableModel):
    def __init__(self, parent, table, db):
        super().__init__(parent, db)

        self.setTable(table)
        self.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.select()

from PySide6.QtSql import QSqlTableModel

from sql.db_manager import create_connection


class TableModel(QSqlTableModel):
    def __init__(self, parent, table):
        db = create_connection()
        super().__init__(parent, db)

        self.setTable(table)
        self.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.select()

from PySide6.QtSql import QSqlTableModel

from sql.db_manager import create_connection


class ClientsTableModel(QSqlTableModel):
    def __init__(self, parent):
        db = create_connection()
        super().__init__(parent, db)

        self.setTable("clients")
        self.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.select()

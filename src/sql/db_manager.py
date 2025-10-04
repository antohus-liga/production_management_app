from PySide6.QtSql import QSqlDatabase

from sql.tables import db_path


def create_connection() -> QSqlDatabase:
    path = db_path

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(path)

    if not db.open():
        raise RuntimeError("Failed to open database")
    return db

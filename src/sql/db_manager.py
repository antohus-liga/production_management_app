from PySide6.QtSql import QSqlDatabase

from sql.tables import db_path


def create_connection() -> QSqlDatabase:
    path = db_path

    if QSqlDatabase.contains("qt_sql_default_connection"):
        db = QSqlDatabase.database("qt_sql_default_connection")
    else:
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(path)

    if not db.isOpen():
        if not db.open():
            raise RuntimeError("Failed to open database")
    return db

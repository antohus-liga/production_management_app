from PySide6.QtSql import QSqlDatabase, QSqlQuery

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


def recalc_product_quantities():
    """Recalculate PRODUCTS.QUANTITY from PRODUCTION."""
    sql = """
        UPDATE PRODUCTS
        SET QUANTITY = COALESCE((
            SELECT SUM(PRODUCTION.QUANTITY_PRODUCED)
            FROM PRODUCTION
            WHERE PRODUCTION.PRODUCT_ID = PRODUCTS.ID
        ), 0)
    """
    query = QSqlQuery()
    if not query.exec(sql):
        print("Error updating quantities:", query.lastError().text())
    else:
        print("Product quantities recalculated.")

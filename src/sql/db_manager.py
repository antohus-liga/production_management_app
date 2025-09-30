from PySide6.QtSql import QSqlDatabase
from sqlalchemy.orm import sessionmaker

from sql.tables import (ClientObj, MaterialObj, MovementInObj, MovementOutObj,
                        ProductObj, SupplierObj, db_path, engine)

Session = sessionmaker(bind=engine)
session = Session()


def create_connection() -> QSqlDatabase:
    path = db_path

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(path)
    if not db.open():
        raise RuntimeError("Failed to open database")
    return db

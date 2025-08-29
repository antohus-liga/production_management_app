import logging
import os
import sys

from PySide6.QtWidgets import QApplication, QWidget
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

app = QApplication(sys.argv)

data_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
)
db_path = os.path.join(data_path, "stock_info.db")
logs_path = os.path.join(data_path, "db_logs.log")

logging.basicConfig(
    filename=logs_path,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
engine = create_engine(f"sqlite:///{db_path}")

widget = QWidget()
widget.show()

app.exec()

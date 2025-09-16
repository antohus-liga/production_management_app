import logging
import os
import sys

from PySide6.QtWidgets import QApplication
from sqlalchemy import create_engine

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

app.exec()

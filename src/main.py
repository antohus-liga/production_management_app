import logging
import os
import sys

from PySide6.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

data_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "appdata",
)
logs_path = os.path.join(data_path, "db_logs.log")

logging.basicConfig(
    filename=logs_path,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

widget = QWidget()
widget.show()

app.exec()

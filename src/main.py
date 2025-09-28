import logging
import os
import sys

from PySide6.QtWidgets import QApplication, QHBoxLayout, QPushButton, QWidget

from sql.db_manager import insert
from sql.tables import ClientObj

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

btn = QPushButton("insert")
btn.clicked.connect(
    lambda: insert(
        ClientObj(
            cod_cli="abc",
            name="david",
            city="pvz",
            country="pt",
            phone_number="923984982",
            email="davidnovo1408@gmail.com",
        )
    )
)

layout = QHBoxLayout()
layout.addWidget(btn)
widget.setLayout(layout)

widget.show()

app.exec()

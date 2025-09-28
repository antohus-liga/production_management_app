import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow

app = QApplication(sys.argv)

# data_path = os.path.join(
#     os.path.dirname(__file__),
#     "..",
#     "appdata",
# )
# logs_path = os.path.join(data_path, "db_logs.log")

# logging.basicConfig(
#     filename=logs_path,
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(message)s",
# )
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

main_window = MainWindow()
main_window.show()

app.exec()

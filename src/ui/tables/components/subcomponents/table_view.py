from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHeaderView, QTableView

from ui.tables.components.subcomponents.sql_table_model import TableModel
from ui.tables.components.subcomponents.unsubmitted_highlight import \
    HighlightDelegate


class TableView(QTableView):
    def __init__(self, table, db):
        super().__init__()

        self.model = TableModel(self, table, db)
        self.setModel(self.model)

        self.font = QFont()
        self.font.setPointSize(14)

        self.setFont(self.font)
        self.setEditTriggers(QTableView.DoubleClicked |
                             QTableView.SelectedClicked)
        self.setStyleSheet(
            "QLineEdit { background: palette(base); color: palette(text); }"
        )

        self.delegate = HighlightDelegate(self)
        self.setItemDelegate(self.delegate)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setSelectionBehavior(QTableView.SelectRows)

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from sql.db_manager import recalc_all_quantities, recalc_all_totals
from ui.tables.components.table_widget import TableWidget


class MovementsOutWidget(QWidget):
    values_updated = Signal()

    def __init__(self, stack, db):
        super().__init__()
        self.stack = stack
        self.table_widget = TableWidget(self.stack, "movements_out", db)
        self.table_widget.table_view.model.dataChanged.connect(
            self.trigger_calculus_update
        )

        self.setLayout(self.table_widget.layout)

    def trigger_calculus_update(self):
        recalc_all_quantities()
        recalc_all_totals()
        self.values_updated.emit()

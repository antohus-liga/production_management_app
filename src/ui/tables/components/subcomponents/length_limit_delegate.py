from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QStyledItemDelegate


class LengthLimitedDelegate(QStyledItemDelegate):
    def __init__(self, field_limits: dict[str, int], parent=None):
        super().__init__(parent)
        self.field_limits = field_limits

    def createEditor(self, parent, option, index):
        model = index.model()
        column_name = model.headerData(index.column(), Qt.Horizontal)
        max_len = self.field_limits.get(column_name)

        if max_len == 0:
            return None

        editor = QLineEdit(parent)
        editor.setMaxLength(max_len)

        return editor

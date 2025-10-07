from PySide6.QtWidgets import QStyledItemDelegate


class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return None

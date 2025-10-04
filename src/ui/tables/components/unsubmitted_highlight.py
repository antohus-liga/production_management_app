from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (QApplication, QLineEdit, QStyle,
                               QStyledItemDelegate)


class HighlightDelegate(QStyledItemDelegate):
    new_rows = set()
    deleted_rows = set()

    def paint(self, painter, option, index):
        model = index.model()
        green = self.themed_color(QPalette.Base, QColor(168, 237, 168))
        red = self.themed_color(QPalette.Base, QColor(237, 152, 152))
        blue = self.themed_color(QPalette.Base, QColor(161, 164, 237))
        dark_blue = self.themed_color(QPalette.Base, QColor(109, 107, 219))

        row_is_dirty = any(
            model.isDirty(model.index(index.row(), col))
            for col in range(model.columnCount())
        )

        if row_is_dirty:
            painter.save()
            painter.fillRect(option.rect, blue)
            painter.restore()

        if model.isDirty(index):
            painter.save()
            painter.fillRect(option.rect, dark_blue)
            painter.restore()

        if index.row() in self.new_rows:
            painter.fillRect(option.rect, green)

        if index.row() in self.deleted_rows:
            painter.fillRect(option.rect, red)

        super().paint(painter, option, index)

    def themed_color(self, role, tint):
        base = QApplication.palette().color(role)
        return QColor(
            (base.red() + tint.red()) // 2,
            (base.green() + tint.green()) // 2,
            (base.blue() + tint.blue()) // 2,
        )

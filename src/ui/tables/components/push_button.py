from PySide6.QtCore import QSize
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QPushButton


class PushButton(QPushButton):
    def __init__(self, text=None, parent=None):
        super().__init__(text, parent)
        self.font = QFont()
        self.font.setBold(True)
        self.font.setPointSize(16)
        self.setFont(self.font)
        self.setIconSize(QSize(20, 20))

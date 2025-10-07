from PySide6.QtCore import QSize
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget

import ui.resources.resources_rc


class MainMenu(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.font = QFont()
        self.font.setPointSize(28)
        menu_btns: list[QPushButton] = [
            QPushButton("Clients"),
            QPushButton("Suppliers"),
            QPushButton("Materials"),
            QPushButton("Products"),
            QPushButton("Production"),
        ]
        icons = (
            ":/icons/customer-service.png",
            ":/icons/supplier.png",
            ":/icons/raw-material.png",
            ":/icons/product.png",
            ":/icons/production.png",
        )

        layout = QVBoxLayout()
        for i, btn in enumerate(menu_btns):
            btn.clicked.connect(lambda _, idx=i: self.stack.setCurrentIndex(idx + 1))
            btn.setIcon(QIcon(icons[i]))
            btn.setIconSize(QSize(34, 34))
            btn.setFont(self.font)
            layout.addWidget(btn)

        self.setLayout(layout)

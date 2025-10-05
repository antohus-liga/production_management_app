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

        clients_btn = QPushButton("Clients")
        clients_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        clients_btn.setIcon(QIcon(":/icons/customer-service.png"))
        clients_btn.setIconSize(QSize(34, 34))
        clients_btn.setFont(self.font)
        suppliers_btn = QPushButton("Suppliers")
        suppliers_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        suppliers_btn.setIcon(QIcon(":/icons/supplier.png"))
        suppliers_btn.setIconSize(QSize(34, 34))
        suppliers_btn.setFont(self.font)
        materials_btn = QPushButton("Materials")
        materials_btn.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        materials_btn.setIcon(QIcon(":/icons/raw-material.png"))
        materials_btn.setIconSize(QSize(34, 34))
        materials_btn.setFont(self.font)

        layout = QVBoxLayout()
        layout.addWidget(clients_btn)
        layout.addWidget(suppliers_btn)
        layout.addWidget(materials_btn)

        self.setLayout(layout)

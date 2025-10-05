from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget


class MainMenu(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        clients_btn = QPushButton("Clients")
        clients_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        suppliers_btn = QPushButton("Suppliers")
        suppliers_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        materials_btn = QPushButton("Materials")
        materials_btn.clicked.connect(lambda: self.stack.setCurrentIndex(3))

        layout = QVBoxLayout()
        layout.addWidget(clients_btn)
        layout.addWidget(suppliers_btn)
        layout.addWidget(materials_btn)

        self.setLayout(layout)

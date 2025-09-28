from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class ClientsTable(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        label = QLabel("Clients")
        go_back_btn = QPushButton("Go back")
        go_back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(go_back_btn)

        self.setLayout(layout)

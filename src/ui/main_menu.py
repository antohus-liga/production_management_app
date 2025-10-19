from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

import ui.resources.resources_rc


class MainMenu(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        title_font = QFont()
        title_font.setPointSize(32)
        title_font.setBold(True)

        subtitle_font = QFont()
        subtitle_font.setPointSize(12)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Optional app icon at the top
        icon_label = QLabel()
        icon_label.setPixmap(QIcon(":/icons/production.png").pixmap(96, 96))
        icon_label.setAlignment(Qt.AlignCenter)

        title = QLabel("Bem-vindo ao Gestor de Produção")
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel(
            "Utilize as janelas em cima para a navegação entre tabelas")
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignCenter)

        layout.addWidget(icon_label)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.setLayout(layout)

import sys

from PySide6.QtWidgets import QWidget

from tables.ui.uic.ui_product_widget import Ui_ProductTable


class ProductWidget(QWidget, Ui_ProductTable):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

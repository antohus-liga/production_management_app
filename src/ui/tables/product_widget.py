from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QSplitter, QVBoxLayout,
                               QWidget)

from ui.tables.components.subcomponents.push_button import PushButton
from ui.tables.components.subcomponents.table_view import TableView
from ui.tables.components.table_widget import TableWidget


class ProductWidget(QWidget):
    def __init__(self, stack, db):
        super().__init__()
        self.stack = stack

        # Master view: products
        self.master = TableWidget(self.stack, "products", db, "Produtos")

        # Detail view: product_materials filtered by selected product
        self.detail_view = TableView("product_materials", db)

        # Hide product_id column in detail view and auto-fill on insert
        # We assume column order: product_id, material_id, quantity_per_unit
        self.detail_view.setColumnHidden(0, True)

        # Detail controls
        self.detail_label_font = QFont()
        self.detail_label_font.setPointSize(20)

        detail_label = QLabel("Lista de Materiais")
        detail_label.setFont(self.detail_label_font)
        detail_label.setFixedHeight(26)

        self.detail_add_btn = PushButton("Inserir novo registo")
        self.detail_add_btn.setIcon(QIcon(":/icons/plus.png"))
        self.detail_delete_btn = PushButton("Eliminar selecionados")
        self.detail_delete_btn.setIcon(QIcon(":/icons/bin.png"))
        self.detail_delete_all_btn = PushButton("Eliminar todos")
        self.detail_delete_all_btn.setIcon(QIcon(":/icons/bin.png"))

        self.detail_add_btn.clicked.connect(self.detail_insert_row)
        self.detail_delete_btn.clicked.connect(self.detail_delete_selected)
        self.detail_delete_all_btn.clicked.connect(self.detail_delete_all)

        detail_controls = QHBoxLayout()
        detail_controls.addWidget(self.detail_delete_all_btn)
        detail_controls.addWidget(self.detail_add_btn)
        detail_controls.addWidget(self.detail_delete_btn)

        # Layout: master on the left, detail on the right using a splitter
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.addWidget(detail_label)
        right_layout.addWidget(self.detail_view)
        right_layout.addLayout(detail_controls)
        right_panel.setLayout(right_layout)

        splitter = QSplitter()
        splitter.setOrientation(Qt.Horizontal)
        splitter.addWidget(self.master)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 65)
        splitter.setStretchFactor(1, 35)

        root_layout = QVBoxLayout()
        root_layout.addWidget(splitter)
        self.setLayout(root_layout)

        # Connect master selection to filter detail
        sel_model = self.master.table_view.selectionModel()
        sel_model.selectionChanged.connect(self._sync_detail_filter)

        # Refresh detail delegate options when materials change
        materials_model = self._get_materials_model(db)
        if materials_model is not None:
            materials_model.dataChanged.connect(self._refresh_detail_delegates)
            materials_model.rowsInserted.connect(
                self._refresh_detail_delegates)
            materials_model.rowsRemoved.connect(self._refresh_detail_delegates)

        # Ensure initial selection drives the detail
        self._sync_detail_filter()

        # On inserting into detail, auto-set hidden product_id to current master id
        self.detail_view.model.rowsInserted.connect(
            self._assign_product_id_to_detail)

        # Initialize enabled state
        self._update_detail_buttons_enabled()

        # Products no longer have material_id; ensure all columns are visible

    def _current_product_id(self) -> str | None:
        view = self.master.table_view
        index = view.currentIndex()
        if not index.isValid():
            return None
        row = index.row()
        return view.model.index(row, 0).data()

    def _sync_detail_filter(self, *args):
        product_id = self._current_product_id()
        if product_id is None:
            self.detail_view.model.setFilter("1=0")
            self.detail_view.model.select()
            self._update_detail_buttons_enabled()
            return
        self.detail_view.model.setFilter(f"product_id = '{product_id}'")
        self.detail_view.model.select()
        self._update_detail_buttons_enabled()

    def _assign_product_id_to_detail(self, parent_index, first, last):
        product_id = self._current_product_id()
        if product_id is None:
            return
        for row in range(first, last + 1):
            self.detail_view.model.setData(
                self.detail_view.model.index(row, 0), product_id
            )
        if not self.detail_view.model.submitAll():
            print(
                "Detail assign product_id failed:",
                self.detail_view.model.lastError().text(),
            )
        else:
            self.detail_view.model.select()

    def _get_materials_model(self, db):
        # Create a lightweight model to watch materials table changes
        try:
            from PySide6.QtSql import QSqlTableModel

            model = QSqlTableModel(self, db)
            model.setTable("materials")
            model.select()
            return model
        except Exception:
            return None

    def _refresh_detail_delegates(self, *args):
        # Recreate the detail view to force delegates to reload their data
        current_filter = self.detail_view.model.filter()
        db = self.detail_view.model.database()
        self.detail_view.setParent(None)
        self.detail_view = TableView("product_materials", db)
        self.detail_view.setColumnHidden(0, True)
        self.detail_view.model.setFilter(current_filter)
        self.detail_view.model.select()
        # Reconnect handlers
        self.detail_view.model.rowsInserted.connect(
            self._assign_product_id_to_detail)

    def _update_detail_buttons_enabled(self) -> None:
        has_product = self._current_product_id() is not None
        self.detail_add_btn.setEnabled(has_product)
        self.detail_delete_btn.setEnabled(has_product)
        self.detail_delete_all_btn.setEnabled(has_product)

    def detail_insert_row(self) -> None:
        if self._current_product_id() is None:
            return
        row = self.detail_view.model.rowCount()
        self.detail_view.model.insertRow(row)
        # Set product_id immediately and submit
        product_id = self._current_product_id()
        self.detail_view.model.setData(
            self.detail_view.model.index(row, 0), product_id)
        if not self.detail_view.model.submitAll():
            print("Detail insert failed:",
                  self.detail_view.model.lastError().text())
        else:
            self.detail_view.model.select()

    def detail_delete_selected(self) -> None:
        selection = self.detail_view.selectionModel().selectedRows()
        if not selection:
            return
        for index in sorted(selection, key=lambda x: x.row(), reverse=True):
            self.detail_view.model.removeRow(index.row())
        if not self.detail_view.model.submitAll():
            print("Detail delete failed:",
                  self.detail_view.model.lastError().text())
            self.detail_view.model.revertAll()
        else:
            self.detail_view.model.select()

    def detail_delete_all(self) -> None:
        product_id = self._current_product_id()
        if product_id is None:
            return
        db = self.detail_view.model.database()
        query = db.exec(
            f"DELETE FROM product_materials WHERE product_id = '{product_id}'"
        )
        if query.lastError().isValid():
            print("Detail delete all failed:", query.lastError().text())
        self.detail_view.model.select()

from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtWidgets import QComboBox, QStyledItemDelegate, QWidget


class MaterialComboDelegate(QStyledItemDelegate):
    def __init__(self, db: QSqlDatabase, parent: QWidget | None = None):
        super().__init__(parent)
        self.db = db
        self.items: list[tuple[str, str]] = []  # (material_id, description)
        self._load_materials()

    def _load_materials(self) -> None:
        self.items.clear()
        query = QSqlQuery(self.db)
        query.exec("SELECT id FROM materials")
        while query.next():
            mat_id = query.value(0)
            self.items.append(mat_id)

    def createEditor(self, parent: QWidget, option, index):
        # Reload materials to reflect any inserts/edits since delegate creation
        self._load_materials()
        combo = QComboBox(parent)
        # Show and store the material ID
        for mat_id in self.items:
            combo.addItem(mat_id)
        combo.setEditable(False)
        return combo

    def setEditorData(self, editor: QWidget, index):
        current_id = index.data(Qt.EditRole) or index.data(Qt.DisplayRole)
        if not isinstance(editor, QComboBox):
            return super().setEditorData(editor, index)
        # Find the index with matching id (either display text or userData)
        target = editor.findData(current_id)
        if target == -1:
            target = editor.findText(str(current_id))
        if target >= 0:
            editor.setCurrentIndex(target)

    def setModelData(self, editor: QWidget, model, index):
        if not isinstance(editor, QComboBox):
            return super().setModelData(editor, model, index)
        mat_id = editor.currentData() or editor.currentText()
        model.setData(index, mat_id, Qt.EditRole)

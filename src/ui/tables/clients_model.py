from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QColor


class ClientsTableModel(QAbstractTableModel):
    def __init__(self, client_data):
        super().__init__()
        self.load_data(client_data)

    def load_data(self, data):
        (
            self.input_cod_cli,
            self.input_name,
            self.input_city,
            self.input_country,
            self.input_phone,
            self.input_email,
        ) = (
            [],
            [],
            [],
            [],
            [],
            [],
        )
        for client in data:
            self.input_cod_cli.append(client.cod_cli)
            self.input_name.append(client.name)
            self.input_city.append(client.city)
            self.input_country.append(client.country)
            self.input_phone.append(client.phone)
            self.input_email.append(client.email)

        self.clients = [
            self.input_cod_cli,
            self.input_name,
            self.input_city,
            self.input_country,
            self.input_phone,
            self.input_email,
        ]
        self.column_count = 6
        self.row_count = len(self.input_cod_cli)

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ("Client Code", "Name", "City", "Country", "Phone", "Email")[section]
        else:
            return f"{section}"

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            return f"{self.clients[column][row]}"
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None

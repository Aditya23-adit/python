from PySide6.QtWidgets import (
    QTableWidget,
    QHeaderView,
    QAbstractItemView
)


class TableComponent(QTableWidget):

    def __init__(self):
        super().__init__()

        self.setup_table()

    def setup_table(self):

        self.setColumnCount(9)

        self.setHorizontalHeaderLabels([
            "Material",
            "Supplier",
            "PO Number",
            "LOT Number",
            "Receive Date",
            "Expired Date",
            "Qty",
            "Production Month",
            "Copy"
        ])

        self.setRowCount(15)

        header = self.horizontalHeader()

        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(True)

        self.verticalHeader().setDefaultSectionSize(30)

        self.setAlternatingRowColors(True)

        self.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.setEditTriggers(
            QAbstractItemView.AllEditTriggers
        )
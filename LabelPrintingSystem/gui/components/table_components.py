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
        # Default column width
        self.setColumnWidth(0, 250)
        self.setColumnWidth(1, 250)
        self.setColumnWidth(2, 130)
        self.setColumnWidth(3, 130)
        self.setColumnWidth(4, 120)
        self.setColumnWidth(5, 120)
        self.setColumnWidth(6, 60)
        self.setColumnWidth(7, 120)
        self.setColumnWidth(8, 60)

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
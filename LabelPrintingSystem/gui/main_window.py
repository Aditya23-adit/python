from PySide6.QtWidgets import QMainWindow

from gui.layouts import MainLayout
from gui.styles import APP_STYLE

from gui.components.table_components import TableComponent
from gui.components.button_components import ButtonComponent
from gui.components.print_components import PrintComponent
from gui.components.status_components import StatusComponent

from PySide6.QtWidgets import QFileDialog, QTableWidgetItem
from excel_import import import_excel

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setup_window()

        self.create_components()

        self.create_layout()

        self.connect_event()

        self.setStyleSheet(APP_STYLE)

    def setup_window(self):

        self.setWindowTitle("STJ LABEL PRINTER 10 x 10")

        self.resize(1400, 750)

    def create_components(self):

        self.table = TableComponent()

        self.buttons = ButtonComponent()

        self.print_panel = PrintComponent()

        self.status = StatusComponent()

    def create_layout(self):

        self.layout = MainLayout(
            self.table,
            self.buttons,
            self.print_panel
        )

        self.setCentralWidget(self.layout)

        self.setStatusBar(self.status)

    def connect_event(self):

        self.buttons.btn_add.clicked.connect(self.add_row)

        self.buttons.btn_delete.clicked.connect(self.delete_row)

        self.buttons.btn_clear.clicked.connect(self.clear_row)
        
        self.buttons.btn_import.clicked.connect(self.import_excel)

    ####################################################
    # EVENT
    ####################################################

    def add_row(self):

        row = self.table.rowCount()

        self.table.insertRow(row)

    def delete_row(self):

        row = self.table.currentRow()

        if row >= 0:

            self.table.removeRow(row)

    def clear_row(self):

        self.table.clearContents()

    def import_excel(self):

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Import Excel",
            "",
            "Excel Files (*.xlsx *.xls)"
        )

        if not file_name:
            return

        rows = import_excel(file_name)

        self.table.setRowCount(len(rows))

        for r, row_data in enumerate(rows):

            for c, value in enumerate(row_data):

                item = QTableWidgetItem(str(value))

                self.table.setItem(r, c, item)

        self.status.showMessage(
            f"{len(rows)} data berhasil diimport."
        )
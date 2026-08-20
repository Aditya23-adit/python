from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout
)
data_excel = []


def import_data():
    global data_excel

    file = filedialog.askopenfilename(
        filetypes=[("Excel Files", "*.xlsx *.xls")]
    )

    if not file:
        return

    data_excel = import_excel(file)

    print(data_excel)

class ButtonComponent(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QHBoxLayout(self)

        self.btn_add = QPushButton("Add")
        self.btn_delete = QPushButton("Delete")
        self.btn_import = QPushButton("Import Excel")
        self.btn_clear = QPushButton("Clear")

        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_delete)
        layout.addWidget(self.btn_import)
        layout.addWidget(self.btn_clear)

        layout.addStretch()
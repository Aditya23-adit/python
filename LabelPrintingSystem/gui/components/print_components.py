from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QComboBox,
    QCheckBox,
    QHBoxLayout
)


class PrintComponent(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QHBoxLayout(self)

        self.cmb_printer = QComboBox()

        self.chk_preview = QCheckBox(
            "Preview sebelum print"
        )

        self.lbl_total_data = QLabel(
            "Total Data : 0"
        )

        self.lbl_total_label = QLabel(
            "Total Label : 0"
        )

        self.btn_preview = QPushButton("Preview")

        self.btn_print = QPushButton("Print")

        layout.addWidget(QLabel("Printer"))

        layout.addWidget(self.cmb_printer)

        layout.addWidget(self.chk_preview)

        layout.addStretch()

        layout.addWidget(self.lbl_total_data)

        layout.addWidget(self.lbl_total_label)

        layout.addSpacing(20)

        layout.addWidget(self.btn_preview)

        layout.addWidget(self.btn_print)
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QCheckBox,
    QPushButton
)

from PySide6.QtPrintSupport import QPrinterInfo


class PrintComponent(QWidget):

    def __init__(self):

        super().__init__()

        # ==================================================
        # TEMPLATE
        # ==================================================

        self.lbl_template = QLabel(
            "Template:"
        )

        self.cmb_template = QComboBox()

        self.btn_import_template = QPushButton(
            "Import Template"
        )

        # ==================================================
        # PRINTER
        # ==================================================

        self.lbl_printer = QLabel(
            "Printer:"
        )

        self.cmb_printer = QComboBox()

        # Load printer
        self.load_printers()

        # ==================================================
        # PREVIEW
        # ==================================================

        #self.chk_preview = QCheckBox(
        #    "Preview sebelum print"
        #)

        # ==================================================
        # TOTAL
        # ==================================================

        #self.lbl_total_data = QLabel(
        #    "Total Data: 0"
        #)

        #self.lbl_total_label = QLabel(
        #    "Total Label: 0"
        #)

        # ==================================================
        # BUTTON
        # ==================================================

        self.btn_preview = QPushButton(
            "Preview"
        )

        self.btn_print = QPushButton(
            "Print"
        )

        # ==================================================
        # MAIN LAYOUT
        # ==================================================

        layout = QVBoxLayout()

        # ==================================================
        # TEMPLATE
        # ==================================================

        template_layout = QHBoxLayout()

        template_layout.addWidget(
            self.lbl_template
        )

        template_layout.addWidget(
            self.cmb_template
        )

        template_layout.addWidget(
            self.btn_import_template
        )

        layout.addLayout(
            template_layout
        )

        # ==================================================
        # PRINTER
        # ==================================================

        printer_layout = QHBoxLayout()

        printer_layout.addWidget(
            self.lbl_printer
        )

        printer_layout.addWidget(
            self.cmb_printer
        )

        layout.addLayout(
            printer_layout
        )

        # ==================================================
        # TOTAL
        # ==================================================

        #layout.addWidget(
        #    self.lbl_total_data
        #)

        #layout.addWidget(
        #    self.lbl_total_label
        #)

        # ==================================================
        # PREVIEW
        # ==================================================

        #layout.addWidget(
        #    self.chk_preview
        #)

        # ==================================================
        # BUTTON
        # ==================================================

        button_layout = QHBoxLayout()

        button_layout.addWidget(
            self.btn_preview
        )

        button_layout.addWidget(
            self.btn_print
        )

        layout.addLayout(
            button_layout
        )

        self.setLayout(
            layout
        )

    # ==================================================
    # LOAD PRINTERS
    # ==================================================

    def load_printers(self):

        self.cmb_printer.clear()

        printers = QPrinterInfo.availablePrinters()

        for printer in printers:

            self.cmb_printer.addItem(
                printer.printerName()
            )

        # ==================================================
        # NO PRINTER
        # ==================================================

        if not printers:

            self.cmb_printer.addItem(
                "Tidak ada printer"
            )
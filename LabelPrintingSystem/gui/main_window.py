from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QTableWidgetItem,
    QMessageBox
)
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices, QIcon

from gui.layouts import MainLayout
from gui.styles import APP_STYLE
from gui.components.table_components import TableComponent
from gui.components.button_components import ButtonComponent
from gui.components.print_components import PrintComponent
from gui.components.status_components import StatusComponent

from excel_import import import_excel
from label.models.label_repository import LabelRepository

from printing.pdf_generator import PdfGenerator
from printing.pdf_printer import PdfPrinter
from printing.template_manager import TemplateManager


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.template_manager = TemplateManager()
        self.pdf_printer = PdfPrinter()

        self.setup_window()
        self.create_components()
        self.create_layout()
        self.connect_events()
        self.load_templates()

        self.setStyleSheet(APP_STYLE)

    # ==================================================
    # WINDOW
    # ==================================================

    def setup_window(self):

        logo = (
            Path(__file__).resolve().parent.parent
            / "label"
            / "assets"
            / "img"
            / "logo.png"
        )

        self.setWindowIcon(QIcon(str(logo)))
        self.setWindowTitle("STJ LABEL PRINTER 10 x 10")
        self.resize(1400, 750)

    # ==================================================
    # COMPONENTS
    # ==================================================

    def create_components(self):

        self.table = TableComponent()
        self.buttons = ButtonComponent()
        self.print_panel = PrintComponent()
        self.status = StatusComponent()

    # ==================================================
    # LAYOUT
    # ==================================================

    def create_layout(self):

        self.layout = MainLayout(
            self.table,
            self.buttons,
            self.print_panel
        )

        self.setCentralWidget(self.layout)
        self.setStatusBar(self.status)

    # ==================================================
    # EVENTS
    # ==================================================

    def connect_events(self):

        self.buttons.btn_add.clicked.connect(self.add_row)
        self.buttons.btn_delete.clicked.connect(self.delete_row)
        self.buttons.btn_clear.clicked.connect(self.clear_table)
        self.buttons.btn_import.clicked.connect(self.import_excel)

        self.print_panel.btn_preview.clicked.connect(
            self.preview_label
        )

        self.print_panel.btn_print.clicked.connect(
            self.print_labels
        )

        self.print_panel.btn_import_template.clicked.connect(
            self.import_template
        )

    # ==================================================
    # TABLE
    # ==================================================

    def add_row(self):
        self.table.insertRow(self.table.rowCount())

    def delete_row(self):

        row = self.table.currentRow()

        if row >= 0:
            self.table.removeRow(row)

    def clear_table(self):
        self.table.clearContents()

    # ==================================================
    # IMPORT EXCEL
    # ==================================================

    def import_excel(self):

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Import Excel",
            "",
            "Excel Files (*.xlsx *.xls)"
        )

        if not file_name:
            return

        try:

            rows = import_excel(file_name)
            self.table.setRowCount(len(rows))

            for r, row in enumerate(rows):
                for c, value in enumerate(row):

                    self.table.setItem(
                        r,
                        c,
                        QTableWidgetItem(str(value))
                    )

            self.status.showMessage(
                f"{len(rows)} data berhasil diimport."
            )

        except Exception as e:
            self.show_error(
                "Import Error",
                f"Import error: {e}"
            )

    # ==================================================
    # TEMPLATE
    # ==================================================

    def load_templates(self):

        try:

            combo = self.print_panel.cmb_template
            current = combo.currentText()

            templates = self.template_manager.get_templates()

            combo.clear()

            for template in templates:
                combo.addItem(
                    template.stem,
                    str(template)
                )

            index = combo.findText(current)

            if index >= 0:
                combo.setCurrentIndex(index)

            self.status.showMessage(
                f"Total Template : {len(templates)}"
                if templates
                else "Belum ada template."
            )

        except Exception as e:

            self.show_error(
                "Template Error",
                f"Template error: {e}"
            )

    def import_template(self):

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Import Template",
            "",
            "Python Template (*.py)"
        )

        if not file_name:
            return

        try:

            destination = self.template_manager.import_template(
                file_name
            )

            self.template_manager.load_template(
                destination.stem
            )

            self.load_templates()

            combo = self.print_panel.cmb_template
            index = combo.findText(destination.stem)

            if index >= 0:
                combo.setCurrentIndex(index)

            self.status.showMessage(
                f"Import Success : {destination.stem}"
            )

        except Exception as e:

            self.show_error(
                "Template Error",
                f"Import template error: {e}"
            )

    def get_selected_template(self):

        name = self.print_panel.cmb_template.currentText()

        if not name:
            raise ValueError("Pilih Template.")

        return name

    # ==================================================
    # LABEL
    # ==================================================

    def get_labels(self):

        labels = LabelRepository.get_labels(self.table)

        if not labels:
            raise ValueError(
                "No Data."
            )

        return labels

    def get_total_labels(self, labels):

        total = 0

        for label in labels:

            try:
                copies = int(label.copy)
            except (ValueError, TypeError):
                copies = 1

            total += max(copies, 1)

        return total

    # ==================================================
    # PDF
    # ==================================================

    def generate_pdf(self, labels, template_name):

        return PdfGenerator(
            template_name=template_name
        ).create_multiple(labels)

    # ==================================================
    # PREVIEW
    # ==================================================

    def preview_label(self):

        try:

            labels = self.get_labels()
            template = self.get_selected_template()

            pdf_file = self.generate_pdf(
                labels,
                template
            )

            QDesktopServices.openUrl(
                QUrl.fromLocalFile(str(pdf_file))
            )

            self.status.showMessage(
                f"Preview berhasil | "
                f"Data: {len(labels)} | "
                f"Label: {self.get_total_labels(labels)} | "
                f"Template: {template}"
            )

        except Exception as e:

            self.show_error(
                "Preview Error",
                f"Preview error: {e}"
            )

    # ==================================================
    # PRINT
    # ==================================================

    def print_labels(self):

        try:

            labels = self.get_labels()
            template = self.get_selected_template()
            printer = self.print_panel.cmb_printer.currentText()

            if not printer:
                raise ValueError("Printer belum dipilih.")

            pdf_file = self.generate_pdf(
                labels,
                template
            )

            self.pdf_printer.print_pdf(
                pdf_file,
                printer
            )

            self.status.showMessage(
                f"Print berhasil | "
                f"Data: {len(labels)} | "
                f"Label: {self.get_total_labels(labels)} | "
                f"Template: {template} | "
                f"Printer: {printer}"
            )

        except Exception as e:

            self.show_error(
                "Print Error",
                f"Print error: {e}"
            )

    # ==================================================
    # ERROR
    # ==================================================

    def show_error(self, title, message):

        self.status.showMessage(message)
        print(message)

        QMessageBox.critical(
            self,
            title,
            message
        )
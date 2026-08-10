from pathlib import Path
from shutil import copy2

from openpyxl import load_workbook

from printing.mapper import LabelMapper


class TemplateEngine:

    def __init__(self):

        self.template_path = Path("label/assets/templates/Label10x10.xlsx")
        self.output_path = Path("label/assets/templates/temp.xlsx")

        self.workbook = None
        self.worksheet = None

    def create(self):
        """
        Membuat salinan template agar file asli tidak berubah.
        """

        copy2(self.template_path, self.output_path)

        self.workbook = load_workbook(self.output_path)

        self.worksheet = self.workbook.active

    def fill(self, label):

        self.worksheet[LabelMapper.SUPPLIER] = label.supplier
        self.worksheet[LabelMapper.PO_NUMBER] = label.po_number
        self.worksheet[LabelMapper.LOT_NUMBER] = label.lot_number
        self.worksheet[LabelMapper.RECEIVE_DATE] = label.receive_date
        self.worksheet[LabelMapper.EXPIRED_DATE] = label.expired_date
        self.worksheet[LabelMapper.QTY] = label.qty
        self.worksheet[LabelMapper.PRODUCTION_MONTH] = label.production_month

    def save(self):

        self.workbook.save(self.output_path)

        return self.output_path
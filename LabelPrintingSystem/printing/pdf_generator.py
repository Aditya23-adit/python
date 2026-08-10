from pathlib import Path

from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class PdfGenerator:

    # ==================================================
    # CONFIGURATION
    # ==================================================

    DPI = 300

    # 100 x 100 mm @ 300 DPI
    WIDTH = 1181
    HEIGHT = 1181

    # 1 ZPL dot = 72 / 300 point
    DOT_TO_POINT = 72 / 300

    def __init__(self):

        # ==================================================
        # FONT PATH
        # ==================================================

        base_path = (
            Path(__file__).resolve().parent.parent
            / "label"
            / "assets"
            / "fonts"
        )

        comic_regular = base_path / "Comic Sans MS.ttf"
        comic_bold = base_path / "Comic Sans MS Bold.ttf"

        # ==================================================
        # CHECK FONT
        # ==================================================

        if not comic_regular.exists():
            raise FileNotFoundError(
                f"Font tidak ditemukan:\n{comic_regular}"
            )

        if not comic_bold.exists():
            raise FileNotFoundError(
                f"Font tidak ditemukan:\n{comic_bold}"
            )

        # ==================================================
        # REGISTER FONT
        # ==================================================

        if "ComicSansMS" not in pdfmetrics.getRegisteredFontNames():

            pdfmetrics.registerFont(
                TTFont(
                    "ComicSansMS",
                    str(comic_regular)
                )
            )

        if "ComicSansMS-Bold" not in pdfmetrics.getRegisteredFontNames():

            pdfmetrics.registerFont(
                TTFont(
                    "ComicSansMS-Bold",
                    str(comic_bold)
                )
            )

        # ==================================================
        # OUTPUT PATH
        # ==================================================

        self.output_path = (
            Path(__file__).resolve().parent.parent
            / "label"
            / "assets"
            / "preview"
            / "label_preview.pdf"
        )

    # ==================================================
    # COORDINATE
    # ==================================================

    def x(self, value):

        return value * self.DOT_TO_POINT

    def y(self, value):

        """
        ZPL:

            Y = 0 berada di ATAS

        ReportLab:

            Y = 0 berada di BAWAH

        Jadi koordinat Y dibalik.
        """

        return (
            self.HEIGHT - value
        ) * self.DOT_TO_POINT

    # ==================================================
    # DRAW LINE
    # ==================================================

    def line(
        self,
        pdf,
        x1,
        y1,
        x2,
        y2,
        width=2
    ):

        pdf.setLineWidth(
            self.x(width)
        )

        pdf.line(
            self.x(x1),
            self.y(y1),
            self.x(x2),
            self.y(y2)
        )

    # ==================================================
    # DRAW BOX
    # ==================================================

    def box(
        self,
        pdf,
        x,
        y,
        width,
        height,
        thickness=2
    ):

        pdf.setLineWidth(
            self.x(thickness)
        )

        pdf.rect(
            self.x(x),
            self.y(y + height),
            self.x(width),
            self.x(height),
            stroke=1,
            fill=0
        )

    # ==================================================
    # TEXT
    # ==================================================

    def text(
        self,
        pdf,
        x,
        y,
        value,
        font="ComicSansMS",
        size=26
    ):

        pdf.setFont(
            font,
            self.x(size)
        )

        pdf.drawString(
            self.x(x),
            self.y(y + size),
            str(value)
        )

    # ==================================================
    # CENTER TEXT
    # ==================================================

    def center_text(
        self,
        pdf,
        x,
        y,
        width,
        value,
        font="ComicSansMS",
        size=26
    ):

        font_size = self.x(size)

        pdf.setFont(
            font,
            font_size
        )

        text_width = stringWidth(
            str(value),
            font,
            font_size
        )

        text_x = (
            self.x(x)
            + (
                self.x(width)
                - text_width
            ) / 2
        )

        pdf.drawString(
            text_x,
            self.y(y + size),
            str(value)
        )

    # ==================================================
    # CREATE PDF
    # ==================================================

    def create(self, label):

        # ==================================================
        # CREATE OUTPUT DIRECTORY
        # ==================================================

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # ==================================================
        # CREATE PDF
        # ==================================================

        pdf = canvas.Canvas(
            str(self.output_path),
            pagesize=(
                self.x(self.WIDTH),
                self.x(self.HEIGHT)
            )
        )

        # ==================================================
        # OUTER BORDER
        # ==================================================

        self.box(
            pdf,
            20,
            20,
            1141,
            1141,
            3
        )

        # ==================================================
        # TITLE BORDER
        # ==================================================

        self.box(
            pdf,
            20,
            20,
            1141,
            90,
            2
        )

        # ==================================================
        # TITLE
        # Comic Sans MS Bold
        # ==================================================

        self.center_text(
            pdf,
            0,
            30,
            1181,
            "Inspection Sticker Rubber Room",
            "ComicSansMS-Bold",
            38
        )

        # ==================================================
        # TITLE UNDERLINE
        # ==================================================

        self.line(
            pdf,
            330,
            80,
            840,
            80,
            3
        )

        # ==================================================
        # DATA TABLE
        # ==================================================

        # Vertical separator

        self.line(
            pdf,
            475,
            110,
            475,
            480,
            2
        )

        # ==================================================
        # MATERIAL
        # ==================================================

        self.text(
            pdf,
            30,
            120,
            "Nama Material 材料名称",
            "ComicSansMS-Bold",
            26
        )

        self.text(
            pdf,
            495,
            120,
            label.material,
            "ComicSansMS",
            30
        )

        self.line(
            pdf,
            20,
            155,
            1161,
            155,
            2
        )

        # ==================================================
        # SUPPLIER
        # ==================================================

        self.text(
            pdf,
            30,
            165,
            "Nama Supplier 供应商名称",
            "ComicSansMS-Bold",
            26
        )

        self.text(
            pdf,
            495,
            165,
            label.supplier,
            "ComicSansMS",
            30
        )

        self.line(
            pdf,
            20,
            200,
            1161,
            200,
            2
        )

        # ==================================================
        # PO
        # ==================================================

        self.text(
            pdf,
            30,
            210,
            "Nomor PO 订单编号",
            "ComicSansMS-Bold",
            26
        )

        self.text(
            pdf,
            495,
            210,
            label.po_number,
            "ComicSansMS",
            30
        )

        self.line(
            pdf,
            20,
            245,
            1161,
            245,
            2
        )

        # ==================================================
        # LOT
        # ==================================================

        self.text(
            pdf,
            30,
            255,
            "Nomor LOT 材料批号",
            "ComicSansMS-Bold",
            26
        )

        self.text(
            pdf,
            495,
            255,
            label.lot_number,
            "ComicSansMS",
            30
        )

        self.line(
            pdf,
            20,
            290,
            1161,
            290,
            2
        )

        # ==================================================
        # RECEIVE DATE
        # ==================================================

        self.text(
            pdf,
            30,
            300,
            "Tgl Masuk Material 进料日期",
            "ComicSansMS-Bold",
            26
        )

        self.text(
            pdf,
            495,
            300,
            label.receive_date,
            "ComicSansMS",
            30
        )

        self.line(
            pdf,
            20,
            335,
            1161,
            335,
            2
        )

        # ==================================================
        # EXPIRED
        # ==================================================

        self.text(
            pdf,
            30,
            345,
            "Tgl Expired 到期日",
            "ComicSansMS-Bold",
            26
        )

        self.text(
            pdf,
            495,
            345,
            label.expired_date,
            "ComicSansMS",
            30
        )

        self.line(
            pdf,
            20,
            380,
            1161,
            380,
            2
        )

        # ==================================================
        # QTY
        # ==================================================

        self.text(
            pdf,
            30,
            390,
            "Jumlah 数量",
            "ComicSansMS-Bold",
            26
        )

        self.text(
            pdf,
            495,
            390,
            label.qty,
            "ComicSansMS",
            30
        )

        self.line(
            pdf,
            20,
            425,
            1161,
            425,
            2
        )

        # ==================================================
        # PRODUCTION MONTH
        # ==================================================

        self.text(
            pdf,
            30,
            435,
            "Bulan Produksi 生产月份",
            "ComicSansMS-Bold",
            26
        )

        self.text(
            pdf,
            495,
            440,
            label.production_month,
            "ComicSansMS",
            30
        )

        # ==================================================
        # INSPECTION SECTION
        # ==================================================

        self.line(
            pdf,
            20,
            480,
            1161,
            480,
            2
        )

        # ==================================================
        # VERTICAL COLUMNS
        # ==================================================

        self.line(
            pdf,
            475,
            480,
            475,
            1160,
            2
        )

        self.line(
            pdf,
            625,
            480,
            625,
            1160,
            2
        )

        self.line(
            pdf,
            775,
            480,
            775,
            1160,
            2
        )

        # ==================================================
        # RELEASE INSPECTION
        # ==================================================

        self.text(
            pdf,
            30,
            500,
            "Sebelum Release Bahan Material",
            "ComicSansMS-Bold",
            25
        )

        self.text(
            pdf,
            30,
            535,
            "Harus Ditest 材料放行前需检验",
            "ComicSansMS-Bold",
            25
        )

        # ==================================================
        # PASS
        # ==================================================

        self.center_text(
            pdf,
            475,
            510,
            150,
            "PASS",
            "ComicSansMS-Bold",
            30
        )

        # ==================================================
        # FAIL
        # ==================================================

        self.center_text(
            pdf,
            625,
            510,
            150,
            "FAIL",
            "ComicSansMS-Bold",
            30
        )

        # ==================================================
        # FIFO
        # ==================================================

        self.center_text(
            pdf,
            775,
            510,
            385,
            "FIFO",
            "ComicSansMS-Bold",
            30
        )

        # ==================================================
        # RELEASE BOTTOM
        # ==================================================

        self.line(
            pdf,
            20,
            615,
            1161,
            615,
            2
        )

        # ==================================================
        # LABORATORY
        # ==================================================

        self.text(
            pdf,
            30,
            635,
            "Hasil Test Laboratorium 实验室测试结果",
            "ComicSansMS-Bold",
            24
        )

        self.line(
            pdf,
            20,
            708,
            775,
            708,
            2
        )

        # ==================================================
        # VISUAL
        # ==================================================

        self.text(
            pdf,
            30,
            725,
            "Hasil Test Visual",
            "ComicSansMS-Bold",
            24
        )

        self.text(
            pdf,
            30,
            755,
            "目视检测",
            "ComicSansMS-Bold",
            24
        )

        self.line(
            pdf,
            20,
            800,
            775,
            800,
            2
        )

        # ==================================================
        # DIMENSION
        # ==================================================

        self.text(
            pdf,
            30,
            815,
            "Hasil Test Dimensi",
            "ComicSansMS-Bold",
            24
        )

        self.text(
            pdf,
            30,
            845,
            "尺寸规格检测",
            "ComicSansMS-Bold",
            24
        )

        self.line(
            pdf,
            20,
            892,
            775,
            892,
            2
        )

        # ==================================================
        # WORKMANSHIP
        # ==================================================

        self.text(
            pdf,
            30,
            910,
            "Tingkat Kerjakan",
            "ComicSansMS-Bold",
            24
        )

        self.text(
            pdf,
            30,
            940,
            "不良品等级",
            "ComicSansMS-Bold",
            24
        )

        self.line(
            pdf,
            20,
            984,
            775,
            984,
            2
        )

        # ==================================================
        # PACKING
        # ==================================================

        self.text(
            pdf,
            30,
            1002,
            "Packing",
            "ComicSansMS-Bold",
            24
        )

        self.text(
            pdf,
            30,
            1032,
            "包装",
            "ComicSansMS-Bold",
            24
        )

        self.line(
            pdf,
            20,
            1076,
            775,
            1076,
            2
        )

        # ==================================================
        # QC SIGNATURE
        # ==================================================

        self.text(
            pdf,
            30,
            1094,
            "Tandatangan QC",
            "ComicSansMS-Bold",
            24
        )

        self.text(
            pdf,
            30,
            1124,
            "QC签名",
            "ComicSansMS-Bold",
            24
        )

        # ==================================================
        # QIP
        # ==================================================

        pdf.setFont(
            "ComicSansMS-Bold",
            self.x(18)
        )

        pdf.drawString(
            self.x(780),
            self.y(1170 + 18),
            "QIP/APP/0300/00-APPENDIX-3"
        )

        # ==================================================
        # SAVE
        # ==================================================

        pdf.save()

        return self.output_path
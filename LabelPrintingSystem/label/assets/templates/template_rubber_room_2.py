from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth


class PdfTemplate:

    NAME = "template_rubber_room_2"

    DPI = 300
    WIDTH = 1181
    HEIGHT = 1181
    DOT_TO_POINT = 72 / DPI

    SHIFT_Y = 5
    BOTTOM_BORDER = 1155

    # ============================================================
    # DATA TABLE
    # ============================================================

    DATA_LEFT = 495
    DATA_RIGHT = 1161
    DATA_PADDING = 10
    DATA_ROW_HEIGHT = 55
    DATA_START_Y = 110
    DATA_END_Y = DATA_START_Y + (8 * DATA_ROW_HEIGHT)

    # ============================================================
    # FONT
    # ============================================================

    FONT_REGULAR = "ComicSansMS"
    FONT_BOLD = "ComicSansMS-Bold"
    FONT_CHINESE = "Microsoft-JhengHei"
    FONT_CHINESE_BOLD = "MJHB"

    FONT_SIZE_TITLE = 38
    FONT_SIZE_ID = 28
    FONT_SIZE_CHINESE = 40
    FONT_SIZE_DATA = 38
    FONT_SIZE_PASS_FAIL = 45
    FONT_SIZE_QIP = 18

    FONT_FILES = {
        "ComicSansMS": "Comic Sans MS.ttf",
        "ComicSansMS-Bold": "Comic Sans MS Bold.ttf",
        "Microsoft-JhengHei": "Microsoft-JhengHei.ttf",
        "MJHB": "MJHB.ttf",
    }

    def __init__(self):
        self.font_path = (
            Path(__file__).resolve().parent.parent / "fonts"
        )
        self.register_fonts()

    def register_fonts(self):
        registered = pdfmetrics.getRegisteredFontNames()

        for name, filename in self.FONT_FILES.items():
            path = self.font_path / filename

            if not path.exists():
                raise FileNotFoundError(
                    f"Font tidak ditemukan.\n\n"
                    f"Font Name:\n{name}\n\n"
                    f"File:\n{path}"
                )

            if name not in registered:
                pdfmetrics.registerFont(
                    TTFont(name, str(path))
                )

    # ============================================================
    # COORDINATE
    # ============================================================

    def x(self, value):
        return value * self.DOT_TO_POINT

    def y(self, value):
        return (self.HEIGHT - value) * self.DOT_TO_POINT

    def up(self, value):
        return value - self.SHIFT_Y

    def safe_text(self, value):
        return "" if value is None else str(value)

    # ============================================================
    # TEXT CLIPPING
    # ============================================================

    def clip_text(self, value, font, size, max_width):
        value = self.safe_text(value)

        if not value:
            return ""

        font_size = self.x(size)
        max_width = self.x(max_width)

        if stringWidth(value, font, font_size) <= max_width:
            return value

        left = 0
        right = len(value)

        while left < right:
            mid = (left + right + 1) // 2

            if stringWidth(
                value[:mid],
                font,
                font_size
            ) <= max_width:
                left = mid
            else:
                right = mid - 1

        return value[:left]

    # ============================================================
    # BASIC TEXT
    # ============================================================

    def text(self, pdf, x, y, value, font, size):
        value = self.safe_text(value)

        pdf.setFont(
            font,
            self.x(size)
        )

        pdf.drawString(
            self.x(x),
            self.y(self.up(y + size)),
            value
        )

    def center_text(
        self,
        pdf,
        x,
        y,
        width,
        value,
        font,
        size
    ):
        value = self.safe_text(value)

        font_size = self.x(size)

        pdf.setFont(font, font_size)

        text_width = stringWidth(
            value,
            font,
            font_size
        )

        text_x = (
            self.x(x)
            + (self.x(width) - text_width) / 2
        )

        pdf.drawString(
            text_x,
            self.y(self.up(y + size)),
            value
        )

    def vertical_center_text(
        self,
        pdf,
        x,
        y,
        height,
        value,
        font,
        size
    ):
        value = self.safe_text(value)

        font_size = self.x(size)

        pdf.setFont(font, font_size)

        center_y = y + height / 2

        text_y = (
            self.y(center_y + size / 2)
            + font_size * 0.25
        )

        pdf.drawString(
            self.x(x),
            text_y,
            value
        )

    # ============================================================
    # FONT HELPERS
    # ============================================================

    def id_txt(self, pdf, x, y, value):
        return self.text(
            pdf, x, y, value,
            self.FONT_BOLD,
            self.FONT_SIZE_ID
        )

    def ch_txt(self, pdf, x, y, value):
        return self.text(
            pdf, x, y, value,
            self.FONT_CHINESE_BOLD,
            self.FONT_SIZE_CHINESE
        )

    def ch_txt1(self, pdf, x, y, value):
        return self.text(
            pdf, x, y, value,
            self.FONT_CHINESE,
            self.FONT_SIZE_CHINESE
        )

    def data_txt(self, pdf, x, y, value):
        return self.text(
            pdf, x, y, value,
            self.FONT_REGULAR,
            self.FONT_SIZE_DATA
        )

    def title_txt(self, pdf, x, y, width, value):
        return self.center_text(
            pdf, x, y, width, value,
            self.FONT_BOLD,
            self.FONT_SIZE_TITLE
        )

    def pass_fail_txt(
        self,
        pdf,
        x,
        y,
        width,
        value
    ):
        return self.center_text(
            pdf, x, y, width, value,
            self.FONT_BOLD,
            self.FONT_SIZE_PASS_FAIL
        )

    def qip_txt(self, pdf, x, y, value):
        pdf.setFont(
            self.FONT_REGULAR,
            self.x(self.FONT_SIZE_QIP)
        )

        pdf.drawString(
            self.x(x),
            self.y(y + self.FONT_SIZE_QIP),
            self.safe_text(value)
        )

    # ============================================================
    # VERTICAL FONT HELPERS
    # ============================================================

    def id_vtxt(
        self,
        pdf,
        x,
        y,
        height,
        value
    ):
        return self.vertical_center_text(
            pdf,
            x,
            y,
            height,
            value,
            self.FONT_BOLD,
            self.FONT_SIZE_ID
        )

    def ch_vtxt(
        self,
        pdf,
        x,
        y,
        height,
        value
    ):
        return self.vertical_center_text(
            pdf,
            x,
            y,
            height,
            value,
            self.FONT_CHINESE_BOLD,
            self.FONT_SIZE_CHINESE
        )

    def ch_vtxt1(
        self,
        pdf,
        x,
        y,
        height,
        value
    ):
        return self.vertical_center_text(
            pdf,
            x,
            y,
            height,
            value,
            self.FONT_CHINESE_BOLD,
            self.FONT_SIZE_CHINESE
        )

    def data_vtxt(
        self,
        pdf,
        x,
        y,
        height,
        value
    ):
        value = self.clip_text(
            value,
            self.FONT_REGULAR,
            self.FONT_SIZE_DATA,
            self.DATA_RIGHT - x - self.DATA_PADDING
        )

        return self.vertical_center_text(
            pdf,
            x,
            y,
            height,
            value,
            self.FONT_REGULAR,
            self.FONT_SIZE_DATA
        )

    # ============================================================
    # LINE / BOX
    # ============================================================

    def line(
        self,
        pdf,
        x1,
        y1,
        x2,
        y2,
        width=2
    ):
        pdf.setLineWidth(self.x(width))

        pdf.line(
            self.x(x1),
            self.y(self.up(y1)),
            self.x(x2),
            self.y(self.up(y2))
        )

    def box(
        self,
        pdf,
        x,
        y,
        width,
        height,
        thickness=2
    ):
        pdf.setLineWidth(self.x(thickness))

        pdf.rect(
            self.x(x),
            self.y(self.up(y + height)),
            self.x(width),
            self.x(height),
            stroke=1,
            fill=0
        )

    # ============================================================
    # DATA TABLE
    # ============================================================

    def draw_data_table(self, pdf, label):

        rows = [
            (
                "Nama Material",
                "材料名称",
                240,
                label.material
            ),
            (
                "Nama Supplier",
                "供应商名称",
                240,
                label.supplier
            ),
            (
                "Nomor PO",
                "订单编号",
                180,
                label.po_number
            ),
            (
                "Nomor LOT",
                "材料批号",
                195,
                label.lot_number
            ),
            (
                "Tgl Masuk Material",
                "进料日期",
                305,
                label.receive_date
            ),
            (
                "Tgl Expired",
                "到期日",
                195,
                label.expired_date
            ),
            (
                "Jumlah",
                "数量",
                140,
                label.qty
            ),
            (
                "Bulan Produksi",
                "生产月份",
                235,
                label.production_month
            ),
        ]

        self.line(
            pdf,
            490,
            self.DATA_START_Y,
            490,
            self.DATA_END_Y,
            2
        )

        for i, (id_text, ch_text, ch_x, value) in enumerate(rows):

            y = (
                self.DATA_START_Y
                + i * self.DATA_ROW_HEIGHT
            )

            self.id_vtxt(
                pdf,
                30,
                y,
                self.DATA_ROW_HEIGHT,
                id_text
            )

            (
                self.ch_vtxt1
                if i == 6
                else self.ch_vtxt
            )(
                pdf,
                ch_x,
                y,
                self.DATA_ROW_HEIGHT,
                ch_text
            )

            self.data_vtxt(
                pdf,
                self.DATA_LEFT,
                y,
                self.DATA_ROW_HEIGHT,
                value
            )

            if i < len(rows) - 1:
                self.line(
                    pdf,
                    20,
                    y + self.DATA_ROW_HEIGHT,
                    1161,
                    y + self.DATA_ROW_HEIGHT,
                    2
                )

    # ============================================================
    # DRAW LABEL
    # ============================================================

    def draw_label(self, pdf, label):

        self.box(
            pdf,
            20,
            20,
            1141,
            self.BOTTOM_BORDER - 20,
            3
        )

        self.box(
            pdf,
            20,
            20,
            1141,
            90,
            2
        )

        self.title_txt(
            pdf,
            0,
            30,
            1181,
            "Inspection Sticker Rubber Room"
        )

        self.line(
            pdf,
            280,
            80,
            900,
            80,
            3
        )

        # ========================================================
        # DATA TABLE
        # ========================================================

        self.draw_data_table(pdf, label)
        # ========================================================
        # INSPECTION
        # ========================================================

        inspection_y = self.DATA_END_Y

        self.line(
            pdf,
            20,
            inspection_y,
            1161,
            inspection_y,
            2
        )

        for x in (490, 640, 790):
            self.line(
                pdf,
                x,
                inspection_y,
                x,
                self.BOTTOM_BORDER,
                2
            )

        # ========================================================
        # RELEASE
        # ========================================================

        self.id_txt(
            pdf,
            30,
            inspection_y,
            "Sebelum Release Bahan Material"
        )

        self.id_txt(
            pdf,
            30,
            inspection_y + 30,
            "Harus Ditest"
        )

        self.ch_txt(
            pdf,
            30,
            inspection_y + 60,
            "材料放行前需检验"
        )

        self.pass_fail_txt(
            pdf,
            490,
            inspection_y + 25,
            150,
            "PASS"
        )

        self.pass_fail_txt(
            pdf,
            640,
            inspection_y + 25,
            150,
            "FAIL"
        )

        self.pass_fail_txt(
            pdf,
            790,
            inspection_y + 25,
            385,
            "FIFO"
        )

        # ========================================================
        # RELEASE BOTTOM
        # ========================================================

        release_bottom = inspection_y + 105

        self.line(
            pdf,
            20,
            release_bottom,
            1161,
            release_bottom,
            2
        )

        # ========================================================
        # INSPECTION DETAILS
        # ========================================================

        sections = [
            ("Hasil Test Laboratorium", "实验室测试结果"),
            ("Hasil Test Visual", "目视检测"),
            ("Hasil Test Dimensi", "尺寸规格检测"),
            ("Tingkat Kerijekan", "不良品等级"),
            ("Packing", "包装"),
            ("Tandatangan QC", "QC签名"),
        ]

        section_start = release_bottom + 8

        available_height = (
            self.BOTTOM_BORDER
            - section_start
        )

        section_height = (
            available_height
            / len(sections)
        )

        for i, (id_text, ch_text) in enumerate(sections):

            y = (
                section_start
                + i * section_height
            )

            self.id_txt(
                pdf,
                30,
                y,
                id_text
            )

            self.ch_txt(
                pdf,
                30,
                y + 27,
                ch_text
            )

            if i < len(sections) - 1:

                self.line(
                    pdf,
                    20,
                    y + section_height - 3,
                    790,
                    y + section_height - 3,
                    2
                )

        # ========================================================
        # QIP
        # ========================================================

        self.qip_txt(
            pdf,
            780,
            1150,
            "QIP/APP/0300/00-APPENDIX-3"
        )
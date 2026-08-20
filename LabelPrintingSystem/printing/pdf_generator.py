from pathlib import Path

from reportlab.pdfgen import canvas

from printing.template_manager import (
    TemplateManager
)


class PdfGenerator:

    # ==================================================
    # INIT
    # ==================================================

    def __init__(
        self,
        template_name
    ):

        if not template_name:

            raise ValueError(
                "Template belum dipilih."
            )

        self.template_name = (
            template_name
        )

        # ==================================================
        # TEMPLATE MANAGER
        # ==================================================

        self.template_manager = (
            TemplateManager()
        )

        # ==================================================
        # LOAD TEMPLATE
        # ==================================================

        self.template = (

            self.template_manager
            .load_template(
                template_name
            )
        )

        # ==================================================
        # VALIDATE TEMPLATE
        # ==================================================

        self.validate_template()

        # ==================================================
        # OUTPUT
        # ==================================================

        self.output_path = (

            Path(__file__)
            .resolve()
            .parent
            .parent

            / "label"
            / "assets"
            / "preview"
            / "label_preview.pdf"
        )

    # ==================================================
    # VALIDATE TEMPLATE
    # ==================================================

    def validate_template(self):

        required = [
            "DPI",
            "WIDTH",
            "HEIGHT",
            "DOT_TO_POINT",
            "SHIFT_Y",
            "draw_label"
        ]

        for attribute in required:

            if not hasattr(
                self.template,
                attribute
            ):

                raise ValueError(
                    f"""
Template '{self.template_name}'
tidak memiliki:

{attribute}
"""
                )

    # ==================================================
    # GET PAGE SIZE
    # ==================================================

    def get_page_size(self):

        width = (
            self.template.WIDTH
            * self.template.DOT_TO_POINT
        )

        height = (
            self.template.HEIGHT
            * self.template.DOT_TO_POINT
        )

        return width, height

    # ==================================================
    # CREATE MULTIPLE
    # ==================================================

    def create_multiple(
        self,
        labels
    ):

        if not labels:

            return None

        # ==================================================
        # DIRECTORY
        # ==================================================

        self.output_path.parent.mkdir(

            parents=True,

            exist_ok=True
        )

        # ==================================================
        # PAGE SIZE
        # ==================================================

        width, height = (
            self.get_page_size()
        )

        # ==================================================
        # CREATE PDF
        # ==================================================

        pdf = canvas.Canvas(

            str(
                self.output_path
            ),

            pagesize=(

                width,

                height
            )
        )

        # ==================================================
        # DRAW
        # ==================================================

        for label in labels:

            copy_count = (
                self.get_copy_count(
                    label
                )
            )

            for _ in range(
                copy_count
            ):

                self.template.draw_label(

                    pdf,

                    label
                )

                pdf.showPage()

        # ==================================================
        # SAVE
        # ==================================================

        pdf.save()

        return self.output_path

    # ==================================================
    # COPY COUNT
    # ==================================================

    def get_copy_count(
        self,
        label
    ):

        try:

            copy_count = int(
                label.copy
            )

        except (
            ValueError,
            TypeError
        ):

            copy_count = 1

        if copy_count < 1:

            copy_count = 1

        return copy_count

    # ==================================================
    # CREATE SINGLE
    # ==================================================

    def create(
        self,
        label
    ):

        return self.create_multiple(
            [label]
        )
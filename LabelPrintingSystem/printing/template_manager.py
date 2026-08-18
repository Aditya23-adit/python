from pathlib import Path
import shutil
import importlib.util
from dataclasses import dataclass


@dataclass(frozen=True)
class FontStyle:

    font: str
    size: int

class TemplateManager:

    # ==================================================
    # INIT
    # ==================================================

    def __init__(self):

        self.template_dir = (
            Path(__file__).resolve().parent.parent
            / "label"
            / "assets"
            / "templates"
        )

        self.template_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # ==================================================
    # GET TEMPLATES
    # ==================================================

    def get_templates(self):

        templates = []

        for file in self.template_dir.glob("*.py"):

            # Abaikan file private
            if file.name.startswith("_"):
                continue

            templates.append(file)

        return sorted(
            templates,
            key=lambda x: x.stem.lower()
        )

    # ==================================================
    # GET TEMPLATE NAMES
    # ==================================================

    def get_template_names(self):

        return [
            template.stem
            for template in self.get_templates()
        ]

    # ==================================================
    # IMPORT TEMPLATE
    # ==================================================

    def import_template(self, source_file):

        source = Path(source_file)

        if not source.exists():

            raise FileNotFoundError(
                f"Template tidak ditemukan:\n{source}"
            )

        if source.suffix.lower() != ".py":

            raise ValueError(
                "Template harus berupa file Python (.py)"
            )

        destination = (
            self.template_dir
            / source.name
        )

        shutil.copy2(
            source,
            destination
        )

        return destination

    # ==================================================
    # LOAD TEMPLATE
    # ==================================================

    def load_template(self, template_name):

        template_file = (
            self.template_dir
            / f"{template_name}.py"
        )

        if not template_file.exists():

            raise FileNotFoundError(
                f"Template tidak ditemukan:\n"
                f"{template_file}"
            )

        spec = importlib.util.spec_from_file_location(
            template_name,
            template_file
        )

        if spec is None:

            raise ImportError(
                f"Tidak dapat membaca template: "
                f"{template_name}"
            )

        if spec.loader is None:

            raise ImportError(
                f"Template loader tidak tersedia: "
                f"{template_name}"
            )

        module = importlib.util.module_from_spec(
            spec
        )

        spec.loader.exec_module(
            module
        )

        # ==================================================
        # FIND PdfTemplate
        # ==================================================

        template_class = None

        for name in dir(module):

            obj = getattr(
                module,
                name
            )

            if (
                isinstance(obj, type)
                and name == "PdfTemplate"
            ):

                template_class = obj
                break

        if template_class is None:

            raise ImportError(
                f"Template '{template_name}' "
                f"tidak memiliki class PdfTemplate."
            )

        return template_class()
    

class PdfTemplate:

    ...

    def set_font(
        self,
        pdf,
        style
    ):

        pdf.setFont(
            style.font,
            self.x(style.size)
        )

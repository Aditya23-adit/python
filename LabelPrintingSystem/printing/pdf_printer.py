from pathlib import Path
import subprocess


class PdfPrinter:

    # ==================================================
    # SUMATRA PDF
    # ==================================================

    SUMATRA_PATH = (
        Path(__file__).resolve().parent.parent
        / "tools"
        / "SumatraPDF-3.6.1-64.exe"
    )

    # ==================================================
    # INIT
    # ==================================================

    def __init__(self):

        if not self.SUMATRA_PATH.exists():

            raise FileNotFoundError(
                f"SumatraPDF tidak ditemukan:\n"
                f"{self.SUMATRA_PATH}"
            )

    # ==================================================
    # PRINT PDF
    # ==================================================

    def print_pdf(
        self,
        pdf_path,
        printer_name
    ):

        # ==============================================
        # PATH
        # ==============================================

        pdf_path = Path(pdf_path)

        # ==============================================
        # CHECK PDF
        # ==============================================

        if not pdf_path.exists():

            raise FileNotFoundError(
                f"PDF tidak ditemukan:\n{pdf_path}"
            )

        # ==============================================
        # CHECK PRINTER
        # ==============================================

        if not printer_name:

            raise ValueError(
                "Printer belum dipilih."
            )

        # ==============================================
        # DEBUG
        # ==============================================

        print("----------------------------------------")
        print("PDF PRINT")
        print("----------------------------------------")
        print("Sumatra :", self.SUMATRA_PATH)
        print("PDF     :", pdf_path)
        print("Printer :", printer_name)
        print("----------------------------------------")

        # ==============================================
        # SUMATRA COMMAND
        # ==============================================

        command = [
            str(self.SUMATRA_PATH),
            "-print-to",
            printer_name,
            "-silent",
            str(pdf_path)
        ]

        print("Command:")
        print(command)

        # ==============================================
        # EXECUTE
        # ==============================================

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60
        )

        # ==============================================
        # RESULT
        # ==============================================

        print(
            "Return Code:",
            result.returncode
        )

        if result.stdout:

            print(
                "STDOUT:",
                result.stdout
            )

        if result.stderr:

            print(
                "STDERR:",
                result.stderr
            )

        # ==============================================
        # CHECK ERROR
        # ==============================================

        if result.returncode != 0:

            raise RuntimeError(
                "SumatraPDF gagal melakukan print.\n"
                f"Return Code: {result.returncode}\n"
                f"STDOUT: {result.stdout}\n"
                f"STDERR: {result.stderr}"
            )

        return True
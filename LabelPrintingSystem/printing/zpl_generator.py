from pathlib import Path

class ZplGenerator:
    def __init__(self):
        self.template_path=(
            Path(__file__).resolve().parent.parent
                /"label"
                /"assets"
                /"templates"
                /"label.zpl"
        )

    def load_template(self):
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template Not Found!!!:\n" f"{self.template_path}")
        
        return self.template_path.read_text(encoding="utf-8")

    def generate(self,label):
        zpl = self.load_template()

        zpl = zpl.replace(
            "{{MATERIAL}}",str(label.material or "")
        )
        zpl = zpl.replace(
            "{{SUPPLIER}}",str(label.supplier or "")
        )
        zpl = zpl.replace(
            "{{PO_NUMBER}}",str(label.po_number or "")
        )
        zpl = zpl.replace(
            "{{LOT_NUMBER}}",str(label.lot_number or "")
        )
        zpl = zpl.replace(
            "{{RECEIVE_DATE}}",str(label.receive_date or "")
        )
        zpl = zpl.replace(
            "{{EXPIRED_DATE}}",str(label.expired_date or "")
        )
        zpl = zpl.replace(
            "{{QTY}}",str(label.qty or "")
        )                                       
        zpl = zpl.replace(
            "{{PRODUCTION_MONTH}}",str(label.production_month or "")
        )
        return zpl

    def generate_multiple(self,labels):
        result=[]
        for label in labels:
            zpl = self.generate(label)
            result.append(zpl)
        return result             
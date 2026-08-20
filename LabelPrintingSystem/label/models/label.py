from dataclasses import dataclass

@dataclass
class LabelData:

    material: str = ""

    supplier: str = ""

    po_number: str = ""

    lot_number: str = ""

    receive_date: str = ""

    expired_date: str = ""

    qty: int = 0

    production_month: str = ""

    copy: int = 1
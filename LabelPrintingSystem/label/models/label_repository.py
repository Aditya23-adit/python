from label.models.label import LabelData


class LabelRepository:

    @staticmethod
    def get_labels(table):

        labels = []

        for row in range(table.rowCount()):

            material = table.item(row, 0)
            supplier = table.item(row, 1)
            po_number = table.item(row, 2)
            lot_number = table.item(row, 3)
            receive_date = table.item(row, 4)
            expired_date = table.item(row, 5)
            qty = table.item(row, 6)
            production_month = table.item(row, 7)
            copy = table.item(row, 8)

            # Lewati baris kosong
            if material is None:
                continue

            label = LabelData(
                material=material.text(),
                supplier=supplier.text() if supplier else "",
                po_number=po_number.text() if po_number else "",
                lot_number=lot_number.text() if lot_number else "",
                receive_date=receive_date.text() if receive_date else "",
                expired_date=expired_date.text() if expired_date else "",
                #qty=int(qty.text()) if qty and qty.text() else 0,
                qty=qty.text() if qty else "0",
                production_month=production_month.text() if production_month else "",
                copy=int(copy.text()) if copy and copy.text() else 1
            )

            labels.append(label)

        return labels
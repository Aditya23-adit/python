from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox
)


class MainLayout(QWidget):

    def __init__(
        self,
        table,
        buttons,
        print_panel
    ):
        super().__init__()

        main_layout = QVBoxLayout(self)

        ##################################################
        # DATA
        ##################################################

        group_data = QGroupBox("Data Label")

        data_layout = QVBoxLayout()

        data_layout.addWidget(table)

        data_layout.addWidget(buttons)

        group_data.setLayout(data_layout)

        ##################################################
        # PRINT
        ##################################################

        main_layout.addWidget(group_data)

        main_layout.addWidget(print_panel)

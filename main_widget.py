import binascii
from PySide6 import QtCore, QtWidgets
import font_table

class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent = parent)

        # set layout for main widget
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)
        sub_layout_1 = QtWidgets.QHBoxLayout()
        sub_layout_2 = QtWidgets.QHBoxLayout()

        self.file_import_button = QtWidgets.QPushButton('导入字库文件')
        sub_layout_1.addWidget(self.file_import_button)
        self.file_import_button.clicked.connect(self.file_import_button_onclick)

        self.filename_label = QtWidgets.QLabel('尚未导入字库文件')
        sub_layout_1.addWidget(self.filename_label)

        self.page_control_spinbox = QtWidgets.QSpinBox()
        self.page_control_spinbox.setMinimum(1)
        self.page_control_spinbox.setEnabled(False)
        sub_layout_1.addWidget(self.page_control_spinbox)
        self.page_control_spinbox.valueChanged.connect(self.on_page_changed)

        main_layout.addLayout(sub_layout_1)

        self.table = font_table.FontTable()
        main_layout.addWidget(self.table)
        self.table.cellClicked.connect(self.on_cell_clicked)

        self.char_display_label = QtWidgets.QLabel()
        self.char_display_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        sub_layout_2.addWidget(self.char_display_label)

        self.neima_display_label = QtWidgets.QLabel()
        self.neima_display_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        sub_layout_2.addWidget(self.neima_display_label)

        self.quweima_display_label = QtWidgets.QLabel()
        self.quweima_display_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        sub_layout_2.addWidget(self.quweima_display_label)

        main_layout.addLayout(sub_layout_2)

    @QtCore.Slot()
    def file_import_button_onclick(self) -> None:
        # get name of the font file
        filename, _ = QtWidgets.QFileDialog.getOpenFileName()
        if filename:  # if user has chosen a font file (not cancelled)
            self.parent().filename = filename  # record its name
            # and display it in the filename label
            self.filename_label.setText(self.parent().filename)
            # draw the first page of font file
            self.table.structure_update(char_size = 16, row_count = 20, column_count = 50)
            self.table.value_update(page = 1, filename = filename)
            # enable page control spinbox
            self.page_control_spinbox.setEnabled(True)

    @QtCore.Slot(int)
    def on_page_changed(self, page: int) -> None:
        self.table.value_update(page = page, filename = self.parent().filename)

    @QtCore.Slot(int, int)
    def on_cell_clicked(self, row: int, column: int) -> None:
        if not self.parent().filename:
            return
        page_index = self.page_control_spinbox.value()
        char_no = (page_index - 1) * 1000 + row * 50+ column
        qu, wei = char_no // 94 + 1, char_no % 94 + 1
        gb2312_bytes = bytes([0xA0 + qu, 0xA0 + wei])
        char = gb2312_bytes.decode(encoding = 'gb2312', errors = 'replace')
        jineima = binascii.hexlify(gb2312_bytes).decode('ascii').upper()
        self.char_display_label.setText(f'字符：{char}')
        self.neima_display_label.setText(f'机内码：0x{jineima}')
        self.quweima_display_label.setText(f'区位码：{qu:02d}{wei:02d}')
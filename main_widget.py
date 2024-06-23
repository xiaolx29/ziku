from PySide6 import QtCore, QtWidgets
import utils, font_table

class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent = parent)

        # init widgets
        self.file_import_button = QtWidgets.QPushButton('导入字库文件')
        self.filename_label = QtWidgets.QLabel('')
        self.page_control_spinbox = QtWidgets.QSpinBox()
        self.page_control_spinbox.setMinimum(1)
        self.page_control_spinbox.setEnabled(False)
        self.page_control_spinbox.setPrefix('第 ')
        self.page_control_spinbox.setSuffix(' 页')
        self.table = font_table.FontTable()
        self.char_display_label = QtWidgets.QLabel()
        self.neima_display_label = QtWidgets.QLabel()
        self.quweima_display_label = QtWidgets.QLabel()

        # set connections
        self.file_import_button.clicked.connect(self.on_file_import_button_clicked)
        self.page_control_spinbox.valueChanged.connect(self.on_page_changed)
        self.table.cellClicked.connect(self.on_cell_clicked)

        # set layout
        sub_layout_1 = QtWidgets.QHBoxLayout()
        sub_layout_1.addWidget(self.file_import_button)
        sub_layout_1.addWidget(self.filename_label)
        sub_layout_1.addWidget(self.page_control_spinbox)
        sub_layout_2 = QtWidgets.QHBoxLayout()
        sub_layout_2.addWidget(self.char_display_label)
        sub_layout_2.addWidget(self.neima_display_label)
        sub_layout_2.addWidget(self.quweima_display_label)
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(sub_layout_1)
        main_layout.addWidget(self.table)
        main_layout.addLayout(sub_layout_2)
        self.setLayout(main_layout)

    @QtCore.Slot()
    def on_file_import_button_clicked(self) -> None:
        # get name of the font file
        filename, _ = QtWidgets.QFileDialog.getOpenFileName()
        if filename:  # if user has chosen a font file (not cancelled)
            self.parent().filename = filename  # record its name
            print(filename)
            print(self.parent().filename)
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

    def display_charinfo(self, charid:int) -> None:
        char, jineima, quweima = utils.get_charinfo_by_charid(charid = charid)
        self.char_display_label.setText(f'字符：{char}')
        self.neima_display_label.setText(f'机内码：{jineima}')
        self.quweima_display_label.setText(f'区位码：{quweima}')

    @QtCore.Slot(int, int)
    def on_cell_clicked(self, row: int, column: int) -> None:
        if not self.parent().filename:
            return
        page = self.page_control_spinbox.value() - 1
        row_count, column_count = self.table.rowCount(), self.table.columnCount()
        charid = (page * row_count + row) * column_count + column
        self.display_charinfo(charid = charid)
    
    def locate_char_in_table(self, charid: int):
        row_count, column_count = self.table.rowCount(), self.table.columnCount()
        page, row, column = charid // (row_count * column_count), charid % (row_count * column_count) // column_count, charid % column_count
        self.page_control_spinbox.setValue(page + 1)
        self.table.setCurrentCell(row, column)
    
    @QtCore.Slot(int, int)
    def on_cell_double_clicked(self, row: int, column: int) -> None:
        if not self.parent().filename:
            return
        print(row, column)
        page = self.page_control_spinbox.value() - 1
        row_count, column_count = self.table.rowCount(), self.table.columnCount()
        charid = (page * row_count + row) * column_count + column
from PySide6 import QtCore, QtWidgets
import char_browse_table, page_control_spinbox, char_info_zone


class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent = parent)

        # init widgets
        self.file_import_button = QtWidgets.QPushButton('导入字库文件')
        self.filename_label = QtWidgets.QLabel()
        self.page_control_spinbox = page_control_spinbox.PageControlSpinbox()
        self.table = char_browse_table.CharBrowseTable()
        self.char_info_zone = char_info_zone.CharInfoZone()

        # set connections
        self.file_import_button.clicked.connect(self.import_file)
        self.page_control_spinbox.valueChanged.connect(self.table_value_update)
        self.table.cellClicked.connect(self.on_cell_clicked)

        # set layout
        hbox_layout = QtWidgets.QHBoxLayout()
        hbox_layout.addWidget(self.file_import_button)
        hbox_layout.addWidget(self.filename_label)
        hbox_layout.addWidget(self.page_control_spinbox)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addLayout(hbox_layout)
        self.layout().addWidget(self.table)
        self.layout().addLayout(self.char_info_zone)
    
    @QtCore.Slot()
    def table_value_update(self):
        page = self.page_control_spinbox.value()
        filename = self.filename_label.text()
        self.table.value_update(page = page, filename = filename)

    @QtCore.Slot()
    def import_file(self) -> None:
        # get name of the font file
        filename, _ = QtWidgets.QFileDialog.getOpenFileName()
        if filename:  # if user has chosen a font file (not cancelled)
            # display the filename string in filenanem label
            self.filename_label.setText(filename)
            # draw the first page of font file on font table
            self.table.structure_update(char_size = 16, row_count = 20, column_count = 50)
            self.table.value_update(page = 1, filename = filename)
            # enable page control spinbox
            self.page_control_spinbox.setEnabled(True)
            self.page_control_spinbox.setValue(1)

    @QtCore.Slot(int, int)
    def on_cell_clicked(self, row: int, column: int) -> None:
        page = self.page_control_spinbox.value() - 1
        charid = self.table.position_to_charid(page_index = page, row_index = row, column_index = column)
        self.char_info_zone.display_charinfo(charid = charid)
    
    def after_search(self, charid: int):
        # show char info
        self.char_info_zone.display_charinfo(charid = charid)
        if not self.filename_label.text():
            return
        # get the position of the char
        page, row, column = self.table.charid_to_position(charid = charid)
        # jump to the page that contains the char
        self.page_control_spinbox.setValue(page + 1)
        # locate the char in the table
        self.table.setCurrentCell(row, column)
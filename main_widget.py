from typing import Final
from PySide6 import QtCore, QtWidgets
import qu_table, qu_control_spinbox, char_info_zone, file_import_dialog

QU_COUNT: Final = 94
WEI_COUNT: Final = 94

class MainWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__(parent = parent)
        self.char_size = 16
        # init widgets
        self.file_import_button = QtWidgets.QPushButton('导入字库文件')
        self.filename_label = QtWidgets.QLabel()
        self.qu_control_spinbox = qu_control_spinbox.QuControlSpinbox()
        self.table = qu_table.QuTable()
        self.char_info_zone = char_info_zone.CharInfoZone()

        # set connections
        self.file_import_button.clicked.connect(self.import_file)
        self.qu_control_spinbox.valueChanged.connect(self.table_value_update)
        self.table.cellClicked.connect(self.on_cell_clicked)

        # set layout
        hbox_layout = QtWidgets.QHBoxLayout()
        hbox_layout.addWidget(self.file_import_button)
        hbox_layout.addWidget(self.filename_label)
        hbox_layout.addWidget(self.qu_control_spinbox)
        vbox_layout = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_layout)
        vbox_layout.addLayout(hbox_layout)
        vbox_layout.addWidget(self.table)
        vbox_layout.addLayout(self.char_info_zone)
    
    @QtCore.Slot()
    def table_value_update(self):
        qu_index = self.qu_control_spinbox.value()
        filename = self.filename_label.text()
        self.table.value_update(filename = filename, qu_index = qu_index, char_size =self.char_size)

    @QtCore.Slot()
    def import_file(self) -> None:
        self.file_import_dialog = file_import_dialog.FileImportDialog()
        self.file_import_dialog.show()
        # # get name of the font file
        # filename, _ = QtWidgets.QFileDialog.getOpenFileName()
        # if filename:  # if user has chosen a font file (not cancelled)
        #     # display the filename string in filenanem label
        #     self.filename_label.setText(filename)
        #     # draw the first page of font file on font table
        #     row_count, column_count = 5, 20
        #     self.table.structure_update(char_size = self.char_size, row_count = row_count, column_count = column_count)
        #     self.table.value_update(filename = filename, qu_index = 1, char_size = self.char_size)
        #     # set qu control spibox enabled and value = 1
        #     self.qu_control_spinbox.on_file_import()

    @QtCore.Slot(int, int)
    def on_cell_clicked(self, row: int, column: int) -> None:
        qu_index = self.qu_control_spinbox.value()
        wei_index = self.table.position_to_weiid(row_index = row, column_index = column)
        self.char_info_zone.display_charinfo(qu_index = qu_index, wei_index = wei_index)
    
    def after_search(self, charid: int):
        # show char info
        qu_index, wei_index = utils.charid_to_quweima(charid = charid)
        self.char_info_zone.display_charinfo(qu_index = qu_index, wei_index = wei_index)
        if not self.filename_label.text():
            return
        # get the position of the char
        row_index, column_index = self.table.weiid_to_position(wei_index = wei_index)
        page_index = charid // WEI_COUNT
        # jump to the page that contains the char
        self.qu_control_spinbox.setValue(page_index + 1)
        # locate the char in the table
        self.table.setCurrentCell(row_index, column_index)
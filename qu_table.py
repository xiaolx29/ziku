from PySide6 import QtCore, QtWidgets, QtGui
import utils

WEI_COUNT = 94

class CellLabel(QtWidgets.QLabel):
    def __init__(self, cell_size):
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(cell_size, cell_size)

class QuTable(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()
        # set minimal section size for headers (to enable smaller cell size)
        self.horizontalHeader().setMinimumSectionSize(0)
        self.verticalHeader().setMinimumSectionSize(0)
    
    def value_update(self, filename: str, qu_index: int, char_size: int) -> None:
        row_count: int = self.rowCount()
        column_count: int = self.columnCount()
        for wei_index in range(1, row_count * column_count + 1):
            if wei_index > WEI_COUNT:  # empty cell
                pixmap: QtGui.QPixmap = QtGui.QPixmap(char_size, char_size)
                pixmap.fill(QtGui.QColor.fromString('#C8C8C8'))
            else:  # non-empty cell
                charid: int = utils.quweima_to_charid(qu = qu_index, wei = wei_index)
                char_pixels: bytes = utils.read_char_pixels_from_file(filename = filename, charid = charid, char_byte_num = 32)
                char_list: list[list[bool]] = utils.char_bytes_to_list(char_bytes = char_pixels, char_size = char_size)
                pixmap: QtGui.QPixmap = utils.char_list_to_pixmap(char_list= char_list)
            row_index, column_index = self.weiid_to_position(wei_index)
            cell_label: QtWidgets.QLabel = self.cellWidget(row_index, column_index)
            cell_label.setPixmap(pixmap)
    
    def set_all_row_height(self, height: int) -> None:
        for row_index in range(self.rowCount()):
            self.setRowHeight(row_index, height)
    
    def set_all_column_width(self, width: int) -> None:
        for column_index in range(self.columnCount()):
            self.setColumnWidth(column_index, width)
    
    def structure_update(self, char_size: int, row_count: int, column_count: int) -> None:
        # update row column count
        self.setRowCount(row_count)
        self.setColumnCount(column_count)
        # update cell size
        self.set_all_row_height(char_size + 4)
        self.set_all_column_width(char_size + 4)
        # update labels
        for cell_index in range(row_count * column_count):
            row_index, column_index = cell_index // column_count, cell_index % column_count
            self.setCellWidget(row_index, column_index, CellLabel(cell_size = char_size + 4))
    
    def weiid_to_position(self, wei_index: int) -> tuple[int, int]:
        column_count: int = self.columnCount()
        row_index, column_index = divmod(wei_index - 1, column_count)
        return row_index, column_index
    
    def position_to_weiid(self, row_index: int, column_index: int) -> int:
        column_count: int = self.columnCount()
        wei_index: int = column_count * row_index + column_index + 1
        return wei_index
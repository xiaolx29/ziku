from PySide6 import QtCore, QtWidgets, QtGui
import utils


class CellLabel(QtWidgets.QLabel):
    def __init__(self, cell_size):
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(cell_size, cell_size)


class CharBrowseTable(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()
        # set minimal section size for headers (to enable smaller cell size)
        self.horizontalHeader().setMinimumSectionSize(0)
        self.verticalHeader().setMinimumSectionSize(0)

    def value_update(self, page: int, filename: str) -> None:
        for cell_index in range(self.rowCount() * self.columnCount()):
            charid = (page - 1) * self.rowCount() * self.columnCount() + cell_index
            if charid >= 94 * 94:
                pixmap = QtGui.QPixmap(16, 16)
                pixmap.fill(QtGui.QColor.fromString('#C8C8C8'))
            else:
                pixmap = utils.char_list_to_pixmap(char_list = utils.char_bytes_to_list(char_bytes = utils.read_char_pixels_from_file(filename = filename, charid = charid, char_byte_num = 32)))
            row_index, column_index = cell_index // self.columnCount(), cell_index % self.columnCount()
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

    def charid_to_position(self, charid: int) -> tuple[int, int, int]:
        row_count, column_count = self.rowCount(), self.columnCount()
        page_index = charid // (row_count * column_count)
        row_index = charid % (row_count * column_count) // column_count
        column_index = charid % column_count
        return page_index, row_index, column_index
    
    def position_to_charid(self, page_index: int, row_index: int, column_index: int) -> int:
        row_count, column_count = self.rowCount(), self.columnCount()
        charid = (page_index * row_count + row_index) * column_count + column_index
        return charid
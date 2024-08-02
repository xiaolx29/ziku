from enum import IntEnum
from functools import partial
import sys
from typing import Final
from PySide6 import QtWidgets, QtGui, QtCore
import utils

CELL_SIZE: Final = 30

class CellBackgroundColor(IntEnum):
    COLOR_TRUE = 0xff000000
    COLOR_FALSE = 0xffffffff
    COLOR_TRUE_TO_FALSE = 0xffff0000
    COLOR_FALSE_TO_TRUE = 0xff00ff00

ColorUpdateStrategy = dict[CellBackgroundColor, CellBackgroundColor]

on_clicked_strategy: ColorUpdateStrategy = {
    CellBackgroundColor.COLOR_TRUE: CellBackgroundColor.COLOR_TRUE_TO_FALSE,
    CellBackgroundColor.COLOR_TRUE_TO_FALSE: CellBackgroundColor.COLOR_TRUE,
    CellBackgroundColor.COLOR_FALSE: CellBackgroundColor.COLOR_FALSE_TO_TRUE,
    CellBackgroundColor.COLOR_FALSE_TO_TRUE: CellBackgroundColor.COLOR_FALSE,
}
clear_strategy: ColorUpdateStrategy = {
    CellBackgroundColor.COLOR_TRUE: CellBackgroundColor.COLOR_TRUE_TO_FALSE,
    CellBackgroundColor.COLOR_FALSE_TO_TRUE: CellBackgroundColor.COLOR_FALSE,
}
reset_strategy: ColorUpdateStrategy = {
    CellBackgroundColor.COLOR_TRUE_TO_FALSE: CellBackgroundColor.COLOR_TRUE,
    CellBackgroundColor.COLOR_FALSE_TO_TRUE: CellBackgroundColor.COLOR_FALSE,
}
save_strategy: ColorUpdateStrategy = {
    CellBackgroundColor.COLOR_FALSE_TO_TRUE: CellBackgroundColor.COLOR_TRUE,
    CellBackgroundColor.COLOR_TRUE_TO_FALSE: CellBackgroundColor.COLOR_FALSE,
}

class CharPixelTable(QtWidgets.QTableWidget):

    def __init__(self):
        super().__init__()
        # disable user selection of cells
        self.setSelectionMode(QtWidgets.QTableWidget.SelectionMode.NoSelection)
        # deal with cellclicked signal
        self.cellClicked.connect(partial(self.set_pixel_color, on_clicked_strategy))

    def set_structure(self, char_size):
        self.char_size = char_size
        self.setRowCount(char_size)
        self.setColumnCount(char_size)
        # add QTableWidgetItem to each cell
        for cell_index in range(char_size ** 2):
            cell_item = QtWidgets.QTableWidgetItem()
            # disable user interaction with item
            cell_item.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
            self.setItem(*divmod(cell_index, char_size), cell_item)
        # set row height and column width
        for row_index in range(char_size):
            self.setRowHeight(row_index, CELL_SIZE)
        for column_index in range(char_size):
            self.setColumnWidth(column_index, CELL_SIZE)
        # size of table = size of cells + size of header + size of frame * 2
        self.setFixedWidth(char_size * CELL_SIZE + self.verticalHeader().width() + self.frameWidth() * 2)
        self.setFixedHeight(char_size * CELL_SIZE + self.horizontalHeader().height() + self.frameWidth() * 2)
    
    def set_char(self, char_bytes: bytes) -> None:
        char_list: list[list[bool]] = utils.char_bytes_to_list(char_bytes = char_bytes)
        # 2d list -> 1d list
        pixel_list: list[bool] = [pixel_bool for row_list in char_list for pixel_bool in row_list]
        for pixel_index, pixel_bool in enumerate(pixel_list):
            color: CellBackgroundColor = CellBackgroundColor.COLOR_TRUE if pixel_bool else CellBackgroundColor.COLOR_FALSE
            self.item(*divmod(pixel_index, self.char_size)).setBackground(QtGui.QColor(color))

    def set_pixel_color(self, color_strategy: ColorUpdateStrategy, row_index: int, column_index: int) -> None:
        cell_item: QtWidgets.QTableWidgetItem = self.item(row_index, column_index)
        curr_color: int = cell_item.background().color().rgb()
        new_color: CellBackgroundColor = color_strategy.get(CellBackgroundColor(curr_color), CellBackgroundColor(curr_color))
        cell_item.setBackground(QtGui.QColor(new_color))
    
    def set_color(self, color_strategy: ColorUpdateStrategy) -> None:
        for pixel_index in range(self.char_size ** 2):
            self.set_pixel_color(color_strategy, *divmod(pixel_index, self.char_size))
    
    def get_char(self) -> list[list[bool]]:
        char_list = []
        for row_index in range(self.char_size):
            row_list = []
            for column_index in range(self.char_size):
                row_list.append(self.item(row_index, column_index).background().color().rgb() == CellBackgroundColor.COLOR_TRUE)
            char_list.append(row_list)
        return char_list

    
if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    clear_button = QtWidgets.QPushButton('clear')
    reset_button = QtWidgets.QPushButton('reset')
    save_button = QtWidgets.QPushButton('save')

    table = CharPixelTable()
    table.set_structure(char_size = 16)
    data = utils.read_char_pixels_from_file(filename = 'ziku_files/HZK/16/HZK16C', charid = 8, char_size = 16)
    table.set_char(data)

    clear_button.clicked.connect(lambda: table.set_color(clear_strategy))
    reset_button.clicked.connect(lambda: table.set_color(reset_strategy))
    save_button.clicked.connect(lambda: table.set_color(save_strategy))

    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(clear_button)
    layout.addWidget(reset_button)
    layout.addWidget(save_button)
    layout.addWidget(table)

    widget = QtWidgets.QWidget()
    widget.setLayout(layout)
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
        
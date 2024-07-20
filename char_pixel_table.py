from functools import partial
from PySide6 import QtWidgets, QtGui, QtCore

CELL_SIZE = 30

class CharPixelTable(QtWidgets.QTableWidget):
    on_clicked_color_strategy_dict = {
        '#000000': '#ff0000',
        '#ff0000': '#000000',
        '#00ff00': '#ffffff',
        '#ffffff': '#00ff00',
    }

    def __init__(self, char_size):
        super().__init__()
        self.char_size = char_size
        self.setRowCount(char_size)
        self.setColumnCount(char_size)

        # add QTableWidgetItem to each cell
        for cell_index in range(char_size ** 2):
            row_index, column_index = divmod(cell_index, char_size)
            cell_item = QtWidgets.QTableWidgetItem()
            # disable user interaction with item
            cell_item.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
            self.setItem(row_index, column_index, cell_item)

        # set row height and column width
        for row_index in range(char_size):
            self.setRowHeight(row_index, CELL_SIZE)
        for column_index in range(char_size):
            self.setColumnWidth(column_index, CELL_SIZE)

        self.setFixedWidth(char_size * CELL_SIZE + self.verticalHeader().width() + self.frameWidth() * 2)
        self.setFixedHeight(char_size * CELL_SIZE + self.horizontalHeader().height() + self.frameWidth() * 2)
        # disable user selection of cells
        self.setSelectionMode(QtWidgets.QTableWidget.SelectionMode.NoSelection)
        # cell clicked -> cell color update
        self.cellClicked.connect(partial(self.cell_color_update, self.on_clicked_color_strategy_dict))

    def cell_color_update(self, color_strategy_dict: dict[str, str], row_index: int, column_index: int) -> None:
        cell_item: QtWidgets.QTableWidgetItem = self.item(row_index, column_index)
        old_color_name: str = cell_item.background().color().name()
        new_color_name: str = color_strategy_dict.get(old_color_name, old_color_name)
        cell_item.setBackground(QtGui.QColor.fromString(new_color_name))

    def color_update(self, color_strategy_dict: dict[str, str]) -> None:
        for cell_index in range(16 * 16):
            row_index, column_index = cell_index // 16, cell_index % 16
            self.cell_color_update(color_strategy_dict = color_strategy_dict, row_index = row_index, column_index = column_index)

    def char_update(self, char_pixels: bytes) -> None:
        for row_index in range(16):
            line_pixels = int.from_bytes(bytes = char_pixels[row_index * 2: row_index * 2 + 2])
            for column_index in range(16):
                item = self.item(row_index, column_index)
                item.setBackground(QtGui.QColor.fromString('#000000') if line_pixels >> 15 - column_index & 1 else QtGui.QColor.fromString('#ffffff'))

    def get_char_pixels(self) -> bytes:
        char_pixels: list[int] = []
        line_pixels = 0
        for cell_index in range(16 * 16):
            row_index, column_index = cell_index // 16, cell_index % 16
            if self.item(row_index, column_index).background().color().name() == '#000000':
                line_pixels = (line_pixels << 1) | 1
            else:
                line_pixels = line_pixels << 1
            if cell_index % 8 == 7:
                char_pixels.append(line_pixels)
                line_pixels = 0
        return bytes(char_pixels)
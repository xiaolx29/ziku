from PySide6 import QtCore, QtWidgets, QtGui
from PIL import Image, ImageQt
import utils

class FontTable(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()
        # set scroll bars on
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        # set minimal section size for headers (to enable smaller cells)
        self.horizontalHeader().setMinimumSectionSize(0)
        self.verticalHeader().setMinimumSectionSize(0)

    def value_update(self, page: int, filename: str) -> None:
        for i in range(1000):
            char_image = Image.new(mode = '1', size = (self.char_size, self.char_size), color = 255)
            utils.draw_character(filename = filename, img = char_image, position = (0, 0), character_index = (page - 1) * 1000 + i)
            pixmap = QtGui.QPixmap.fromImage(ImageQt.ImageQt(char_image))
            self.table_labels[i // 50][i % 50].setPixmap(pixmap)
    
    def structure_update(self, char_size, row_count, column_count):
        self.char_size: int = char_size
        # update row column count
        self.setRowCount(row_count)
        self.setColumnCount(column_count)
        # update cell size
        for row_index in range(row_count):
            self.setRowHeight(row_index, char_size + 4)
        for column_index in range(column_count):
            self.setColumnWidth(column_index, char_size + 4)
        # update labels
        self.table_labels: list[list[QtWidgets.QLabel]] = [[QtWidgets.QLabel() for i in range(column_count)] for j in range(row_count)]
        for i in range(row_count * column_count):
            table_label = self.table_labels[i // column_count][i % column_count]
            table_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            # update label size
            table_label.resize(char_size + 4, char_size + 4)
            # add label to cell
            self.setCellWidget(i // column_count, i % column_count, table_label)



from PySide6 import QtCore, QtWidgets, QtGui
class CharEditWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent = parent)
        self.setWindowTitle("新窗口")
        self.setGeometry(100, 100, 300, 200)
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        self.table = QtWidgets.QTableWidget()
        self.table.setRowCount(16)
        self.table.setColumnCount(16)
        for row_index in range(16):
            self.table.setRowHeight(row_index, 10)
        for column_index in range(16):
            self.table.setColumnWidth(column_index, 10)
        layout.addWidget(self.table)
        self.table.cellClicked.connect(self.on_cell_clicked)

    @QtCore.Slot(int, int)
    def on_cell_clicked(self, row: int, column: int):
        item = self.table.item(row, column)
        print(item.background().color())
        if item.background().color() == QtGui.QColor(0, 0, 0):
            item.setBackground(QtGui.QColor(255, 255, 255))
        else:
            item.setBackground(QtGui.QColor(0, 0, 0))

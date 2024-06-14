import binascii
import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PIL import ImageQt
import utils

class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.Signal(QtCore.QPoint)
    double_clicked = QtCore.Signal(QtCore.QPoint)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        # if left mouse button clicked
        if event.button() == QtCore.Qt.LeftButton:
            # emit a signal and pass mouse position
            self.clicked.emit(event.position().toPoint())
    
    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        # if left mouse button double clicked
        if event.button() == QtCore.Qt.LeftButton:
            pass

class MainWindow(QtWidgets.QMainWindow):
    filename = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle('字库工具')
        self.setGeometry(100, 100, 800, 600)

        self.dock_widget = QtWidgets.QDockWidget('Dockable Window')
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock_widget)

        widget = QtWidgets.QWidget()
        # self.setCentralWidget(central_widget)
        self.dock_widget.setWidget(widget)

        layout = QtWidgets.QGridLayout()
        widget.setLayout(layout)

        self.file_import_button = QtWidgets.QPushButton('导入字库文件')
        layout.addWidget(self.file_import_button, 0, 0)
        self.file_import_button.clicked.connect(self.file_import_button_onclick)

        self.filename_label = QtWidgets.QLabel('尚未导入字库文件')
        layout.addWidget(self.filename_label, 0, 1)

        self.page_control_spinbox = QtWidgets.QSpinBox()
        self.page_control_spinbox.setMinimum(1)
        self.page_control_spinbox.setEnabled(False)
        layout.addWidget(self.page_control_spinbox, 0, 2)
        self.page_control_spinbox.valueChanged.connect(self.change_page)

        self.font_browse_label = ClickableLabel()
        self.font_browse_label.setAlignment(QtCore.Qt.AlignTop)
        layout.addWidget(self.font_browse_label, 1, 0, 1, 3)
        self.font_browse_label.clicked.connect(self.font_browse_label_onclick)

        self.char_display_label = QtWidgets.QLabel()
        self.font_browse_label.setAlignment(QtCore.Qt.AlignTop)
        layout.addWidget(self.char_display_label, 2, 0)

    @QtCore.Slot()
    def file_import_button_onclick(self) -> None:
        # get name of the font file
        filename, _ = QtWidgets.QFileDialog.getOpenFileName()
        if filename:  # if user has chosen a font file (not cancelled)
            self.filename = filename  # record its name
            # and display it in the filename label
            self.filename_label.setText(self.filename)
            # draw the first page of font file
            qimage = ImageQt.ImageQt(utils.draw_page(filename = self.filename, page_index = 0))
            pixmap = QtGui.QPixmap.fromImage(qimage)
            self.font_browse_label.setPixmap(pixmap)
            # enable page control spinbox
            self.page_control_spinbox.setEnabled(True)
            
    @QtCore.Slot(QtCore.QPoint)
    def font_browse_label_onclick(self, pos: QtCore.QPoint) -> None:
        page_index = self.page_control_spinbox.value()
        char_no = (page_index - 1) * 1000 + (pos.y() // 16 * 50+ pos.x() // 16)
        high_byte, low_byte = 0xA1 + char_no // 94, 0xA1 + char_no % 94
        gb2312_bytes = bytes([high_byte, low_byte])
        char = gb2312_bytes.decode(encoding = 'gb2312', errors = 'replace')
        number = binascii.hexlify(gb2312_bytes).decode('ascii').upper()
        self.char_display_label.setText(f'{char} {number}')

    @QtCore.Slot(int)
    def change_page(self, page_index: int) -> None:
        qimage = ImageQt.ImageQt(utils.draw_page(filename = self.filename, page_index = page_index - 1))
        pixmap = QtGui.QPixmap.fromImage(qimage)
        self.font_browse_label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
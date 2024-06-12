import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PIL import ImageQt
import utils

class ClickableLabel(QtWidgets.QLabel):
    def __init__(self, parent = None):
        super().__init__(parent)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        # 检查事件类型是否为鼠标左键点击
        if event.button() == QtCore.Qt.LeftButton:
            local_pos = event.position()
            # 输出坐标
            print(f"Mouse clicked at: ({local_pos.x()}, {local_pos.y()})")
        # 调用基类的mousePressEvent以保持其他行为
        super().mousePressEvent(event)

class MainWindow(QtWidgets.QMainWindow):
    filename = None

    def __init__(self):
        super().__init__()
        # 设置窗口标题和大小
        self.setWindowTitle('字库工具')
        self.setGeometry(100, 100, 400, 300)

        # 创建一个中央部件
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # 创建一个垂直布局
        layout = QtWidgets.QGridLayout()
        central_widget.setLayout(layout)

        # 创建一个按钮
        self.file_import_button = QtWidgets.QPushButton('导入字库文件')
        layout.addWidget(self.file_import_button, 0, 0)
        self.file_import_button.clicked.connect(self.import_file)

        # 创建一个标签
        self.filename_label = QtWidgets.QLabel('尚未导入字库文件')
        layout.addWidget(self.filename_label, 0, 1)

        self.page_control_spinbox = QtWidgets.QSpinBox()
        layout.addWidget(self.page_control_spinbox, 0, 2)

        self.font_browse_label = ClickableLabel()
        layout.addWidget(self.font_browse_label, 1, 0, 1, 3)

    @QtCore.Slot()
    def import_file(self) -> None:
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
            
    @QtCore.Slot(QtCore.QPoint)
    def on_label_clicked(self, point: QtCore.QPoint):
        print(f"Clicked at: {point.x()}, {point.y()}")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
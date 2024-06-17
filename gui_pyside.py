import sys
from PySide6 import QtWidgets
import main_widget

class MainWindow(QtWidgets.QMainWindow):
    filename = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle('字库工具')
        self.setGeometry(100, 100, 800, 400)
        self.setCentralWidget(main_widget.MainWidget(parent = self))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
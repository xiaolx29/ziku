from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PySide6 import QtCore
app = None
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建一个按钮，点击时打开新窗口
        self.button = QPushButton("打开新窗口", self)
        self.button.clicked.connect(self.open_new_window)

        # 设置布局（为了简单起见，这里省略了完整的布局设置）
        # ...

        # 显示主窗口___
        self.show()

    def open_new_window(self):
        # 实例化新窗口类并显示它
        new_window = NewWindow()
        new_window.show()
        new_window.setWindowState(QtCore.Qt.WindowState.WindowMaximized)
        print(new_window.isVisible())


class NewWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 在这里设置新窗口的 UI 组件
        # 例如，可以添加一个标签或其他按钮

        # 设置窗口标题和大小（可选）
        self.setWindowTitle("新窗口")
        self.setGeometry(100, 100, 300, 200)
        self.setVisible(True)
        print('hj')


if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
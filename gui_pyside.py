import sys
from PySide6 import QtWidgets, QtGui, QtCore
import utils, main_widget, char_edit_widget, char_searcher

class MainWindow(QtWidgets.QMainWindow):
    filename = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle('字库工具')
        self.setGeometry(100, 100, 800, 400)

        self.char_edit_window = char_edit_widget.CharEditWidget()
        self.setCentralWidget(main_widget.MainWidget(parent = self))
        self.setMenuBar(QtWidgets.QMenuBar(self))

        self.file_import_action = QtGui.QAction('导入字库')
        self.file_import_action.triggered.connect(self.centralWidget().import_file)
        file_menu = self.menuBar().addMenu('文件')
        file_menu.addAction(self.file_import_action)

        self.search_by_char_action = QtGui.QAction('按字符搜索')
        self.search_by_char_action.triggered.connect(self.search_by_char)
        self.search_action_group = QtGui.QActionGroup(self)
        self.search_action_group.addAction(self.search_by_char_action)
        search_menu = self.menuBar().addMenu('搜索')
        search_menu.addAction(self.search_by_char_action)

        self.about_me_action = QtGui.QAction('关于 我')
        self.about_me_action.triggered.connect(self.about_me)
        self.about_qt_action = QtGui.QAction('关于 Qt')
        self.about_qt_action.triggered.connect(QtWidgets.QApplication.aboutQt)
        about_menu = self.menuBar().addMenu('关于')
        about_menu.addActions([self.about_me_action, self.about_qt_action])

        self.centralWidget().table.cellDoubleClicked.connect(self.open_edit_window)
        self.char_edit_window.char_pixel_updated.connect(self.centralWidget().table_value_update)

    def about_me(self):
        QtWidgets.QMessageBox.about(self, '关于 我', 'xiaolx')

    def search_by_char(self):
        if not (charid := char_searcher.CharSearcher().run()):
            return
        # after searching, do 1: show char info and 2: locate the char in the table
        self.centralWidget().after_search(charid = charid)
    
    @QtCore.Slot(int, int)
    def open_edit_window(self, row, column):
        if not (filename := self.centralWidget().filename_label.text()):
            return
        page = self.centralWidget().page_control_spinbox.value() - 1
        row_count, column_count = self.centralWidget().table.rowCount(), self.centralWidget().table.columnCount()
        charid = (page * row_count + row) * column_count + column
        if charid >= 94 * 94:
            return
        self.char_edit_window.show()
        char_pixels = utils.read_char_pixels_from_file(filename = filename, charid = charid)
        self.char_edit_window.char_update(filename = self.centralWidget().filename_label.text(), charid = charid, char_pixels = char_pixels)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
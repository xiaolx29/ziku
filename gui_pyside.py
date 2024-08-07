from functools import partial
import sys
from typing import Final
from PySide6 import QtWidgets, QtGui, QtCore
import utils, main_widget, char_edit_widget, char_searcher


WEI_COUNT: Final = 94

class MainWindow(QtWidgets.QMainWindow):
    filename = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle('字库工具')
        self.setGeometry(100, 100, 800, 400)

        self.char_edit_window = char_edit_widget.CharEditWidget()
        self.main_widget = main_widget.MainWidget(parent = self)
        self.setCentralWidget(self.main_widget)
        self.setMenuBar(QtWidgets.QMenuBar(self))

        self.file_import_action = QtGui.QAction('导入字库')
        self.file_import_action.triggered.connect(self.main_widget.import_file)
        file_menu = self.menuBar().addMenu('文件')
        file_menu.addAction(self.file_import_action)

        self.search_by_char_action = QtGui.QAction('按字符搜索')
        self.search_by_char_action.triggered.connect(self.search_by_char)
        self.search_action_group = QtGui.QActionGroup(self)
        self.search_action_group.addAction(self.search_by_char_action)
        search_menu = self.menuBar().addMenu('搜索')
        search_menu.addAction(self.search_by_char_action)

        setting_menu = self.menuBar().addMenu('设置')
        set_char_size_menu = setting_menu.addMenu('设置字号')
        self.set_char_group = QtGui.QActionGroup(self)
        self.set_char_group.setExclusive(True)
        for char_size in [12, 14, 16, 24, 32, 40, 48]:
            action = QtGui.QAction(str(char_size), self)
            action.setCheckable(True)
            set_char_size_menu.addAction(action)
            self.set_char_group.addAction(action)
            action.toggled.connect(partial(self.set_char_size, char_size))
        
        self.about_me_action = QtGui.QAction('关于 我')
        self.about_me_action.triggered.connect(self.about_me)
        self.about_qt_action = QtGui.QAction('关于 Qt')
        self.about_qt_action.triggered.connect(QtWidgets.QApplication.aboutQt)
        about_menu = self.menuBar().addMenu('关于')
        about_menu.addActions([self.about_me_action, self.about_qt_action])

        self.main_widget.table.cellDoubleClicked.connect(self.open_edit_window)
        self.char_edit_window.char_pixel_updated.connect(self.main_widget.table_value_update)
    
    def set_char_size(self, char_size: int, action_checked: bool) -> None:
        if not action_checked:
            return
        self.char_size = char_size
        self.main_widget.char_size = char_size
        self.main_widget.table.structure_update(char_size = char_size, row_count = 5, column_count = 20)

    def about_me(self):
        QtWidgets.QMessageBox.about(self, '关于 我', 'xiaolx')

    def search_by_char(self):
        if not (charid := char_searcher.CharSearcher().run()):
            return
        # after searching, do 1: show char info and 2: locate the char in the table
        self.main_widget.after_search(charid = charid)
    
    @QtCore.Slot(int, int)
    def open_edit_window(self, row, column):
        if not (filename := self.main_widget.filename_label.text()):
            return
        qu_index = self.main_widget.qu_control_spinbox.value()
        wei_index = self.main_widget.table.position_to_weiid(row_index = row, column_index = column)
        charid = utils.quweima_to_charid(qu = qu_index, wei = wei_index)
        if wei_index > WEI_COUNT:
            return
        self.char_edit_window.show()
        char_pixels = utils.read_char_pixels_from_file(filename = filename, charid = charid, char_byte_num = 32)
        self.char_edit_window.char_update(filename = self.main_widget.filename_label.text(), charid = charid, char_pixels = char_pixels)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
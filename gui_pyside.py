import codecs
import sys
from PySide6 import QtWidgets, QtGui, QtCore
import utils, main_widget, char_edit_widget

class MainWindow(QtWidgets.QMainWindow):
    filename = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle('字库工具')
        self.setGeometry(100, 100, 800, 400)
        self.main_widget = main_widget.MainWidget(parent = self)
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Vertical)
        self.splitter.addWidget(self.main_widget)
        self.test = char_edit_widget.CharEditWidget(parent = self)
        self.splitter.addWidget(self.test)
        self.setCentralWidget(self.splitter)

        menu_bar = QtWidgets.QMenuBar(self)
        self.setMenuBar(menu_bar)

        self.file_import_action = QtGui.QAction('导入字库')
        self.file_import_action.triggered.connect(self.main_widget.on_file_import_button_clicked)
        file_menu = menu_bar.addMenu('文件')
        file_menu.addAction(self.file_import_action)

        self.search_by_char_action = QtGui.QAction('按字符搜索')
        self.search_by_char_action.triggered.connect(self.search_by_char)
        self.search_action_group = QtGui.QActionGroup(self)
        self.search_action_group.addAction(self.search_by_char_action)
        search_menu = menu_bar.addMenu('搜索')
        search_menu.addAction(self.search_by_char_action)

        self.about_me_action = QtGui.QAction('关于 我')
        self.about_me_action.triggered.connect(self.about_me)
        self.about_qt_action = QtGui.QAction('关于 Qt')
        self.about_qt_action.triggered.connect(QtWidgets.QApplication.aboutQt)
        about_menu = menu_bar.addMenu('关于')
        about_menu.addAction(self.about_me_action)
        about_menu.addAction(self.about_qt_action)

        self.main_widget.table.cellDoubleClicked.connect(self.a)

    def about_me(self):
        QtWidgets.QMessageBox.about(self, '关于 我', 'xiaolx')

    def search_by_char(self):
        text, ok = QtWidgets.QInputDialog.getText(self, '按字符搜索', '请输入要搜索的字符：')
        if not ok:  # cancelled
            return
        if len(text) == 0:  # empty input
            QtWidgets.QMessageBox.warning(self, '搜索错误', '您没有输入任何字符')
            return
        try:
            jineima = utils.char_to_jineima(text[0], errors = 'strict')
        except UnicodeEncodeError:  # the char has no gb2312 coding
            QtWidgets.QMessageBox.warning(self, '搜索错误', '您输入的字符没有G2312编码')
            return
        if len(jineima) == 1:  # the char is half-width (1 byte long)
            QtWidgets.QMessageBox.warning(self, '搜索错误', '您输入的字符没有G2312编码')
            return
        charid = utils.quweima_to_charid(*utils.jineima_to_quweima(jineima))
        # after searching, do 1: show char info and 2: locate the char in the table
        self.main_widget.display_charinfo(charid = charid)
        if self.filename:
            self.main_widget.locate_char_in_table(charid = charid)
    
    @QtCore.Slot(int, int)
    def a(self, row, column):
        if not (filename := self.main_widget.filename_label.text()):
            return
        print(row, column)
        page = self.main_widget.page_control_spinbox.value() - 1
        row_count, column_count = self.main_widget.table.rowCount(), self.main_widget.table.columnCount()
        charid = (page * row_count + row) * column_count + column
        character_data = utils.get_character(filename = filename, character_index = charid)
        for y in range(16):
            line_data = int.from_bytes(bytes = character_data[y * 2: y * 2 + 2])
            print(line_data)
            for x in range(16):
                if (line_data >> (15 - x)) & 1:
                    self.test.table.setItem(y, x, QtWidgets.QTableWidgetItem(''))
                    self.test.table.item(y, x).setBackground(QtGui.QColor(0, 0, 0))
                else:
                    self.test.table.setItem(y, x, QtWidgets.QTableWidgetItem(''))
                    self.test.table.item(y, x).setBackground(QtGui.QColor(255, 255, 255))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
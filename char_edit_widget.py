from PySide6 import QtCore, QtWidgets
import char_pixel_table, utils

class CharEditWidget(QtWidgets.QWidget):
    char_pixel_updated = QtCore.Signal()

    def __init__(self):
        super().__init__()
        # init widgets
        self.table = char_pixel_table.CharPixelTable()
        self.clear_button = QtWidgets.QPushButton('清空')
        self.reset_button = QtWidgets.QPushButton('还原')
        self.save_button = QtWidgets.QPushButton('存储')

        # set button group
        self.button_group = QtWidgets.QButtonGroup()
        self.button_group.addButton(self.clear_button)
        self.button_group.addButton(self.reset_button)
        self.button_group.addButton(self.save_button)

        # set connections
        self.button_group.buttonClicked.connect(self.button_clicked)

        # set layout
        self.hbox_layout = QtWidgets.QHBoxLayout()
        self.hbox_layout.addWidget(self.clear_button)
        self.hbox_layout.addWidget(self.reset_button)
        self.hbox_layout.addWidget(self.save_button)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addLayout(self.hbox_layout)
        self.layout().addWidget(self.table)

    @QtCore.Slot(QtWidgets.QPushButton)
    def button_clicked(self, button: QtWidgets.QPushButton):
        if button == self.save_button:  # if this is the save button and user do not want to save
            reply = QtWidgets.QMessageBox.question(None, "标题", "你确定要执行此操作吗？", QtWidgets.QMessageBox.StandardButton.Yes, QtWidgets.QMessageBox.StandardButton.No)
            if reply == QtWidgets.QMessageBox.StandardButton.No:
                return
        match button:
            case self.clear_button:
                self.table.color_update({'#000000': '#ff0000', '#00ff00': '#ffffff'})
            case self.reset_button:
                self.table.color_update({'#ff0000': '#000000', '#00ff00': '#ffffff'})
            case self.save_button:
                self.table.color_update({'#00ff00': '#000000', '#ff0000': '#ffffff'})
        if button == self.save_button:
            #save to file
            char_pixels = self.table.get_char_pixels()
            utils.write_char_pixels_to_file(filename = self.filename, charid = self.charid, char_pixels = char_pixels)
            self.char_pixel_updated.emit()

    def char_update(self, filename: str, charid: int, char_pixels: bytes):
        self.filename = filename
        self.charid = charid
        self.table.char_update(char_pixels)

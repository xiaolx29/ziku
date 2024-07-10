from PySide6 import QtWidgets
import utils

class CharInfoZone(QtWidgets.QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.character_display_label = QtWidgets.QLabel('字符：')
        self.jineima_display_label = QtWidgets.QLabel('机内码：')
        self.quweima_display_label = QtWidgets.QLabel('区位码：')

        self.addWidget(self.character_display_label)
        self.addWidget(self.jineima_display_label)
        self.addWidget(self.quweima_display_label)

    def display_charinfo(self, charid:int) -> None:
        if charid >= 94 * 94:
            self.character_display_label.setText('字符：')
            self.jineima_display_label.setText('机内码：')
            self.quweima_display_label.setText('区位码：')
            return
        qu, wei = utils.charid_to_quweima(charid = charid)
        jineima = utils.quweima_to_jineima(qu = qu, wei = wei)
        char = utils.jineima_to_char(jineima = jineima, errors = 'replace')
        self.character_display_label.setText(f'字符：{char}')
        self.jineima_display_label.setText(f'机内码：{int.from_bytes(jineima):#X}')
        self.quweima_display_label.setText(f'区位码：{qu:02d} {wei:02d}')

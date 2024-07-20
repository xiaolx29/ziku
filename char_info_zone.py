from typing import Final
from PySide6 import QtWidgets
import utils

WEI_COUNT: Final = 94

class CharInfoZone(QtWidgets.QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.character_display_label = QtWidgets.QLabel('字符：')
        self.jineima_display_label = QtWidgets.QLabel('机内码：')
        self.quweima_display_label = QtWidgets.QLabel('区位码：')

        self.addWidget(self.character_display_label)
        self.addWidget(self.jineima_display_label)
        self.addWidget(self.quweima_display_label)

    def display_charinfo(self, qu_index:int, wei_index: int) -> None:
        if wei_index > WEI_COUNT:
            self.character_display_label.setText('字符：')
            self.jineima_display_label.setText('机内码：')
            self.quweima_display_label.setText('区位码：')
            return
        jineima = utils.quweima_to_jineima(qu = qu_index, wei = wei_index)
        char = utils.jineima_to_char(jineima = jineima, errors = 'replace')
        self.character_display_label.setText(f'字符：{char}')
        self.jineima_display_label.setText(f'机内码：{int.from_bytes(jineima):#X}')
        self.quweima_display_label.setText(f'区位码：{qu_index:02d} {wei_index:02d}')

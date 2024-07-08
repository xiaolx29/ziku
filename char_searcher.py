from PySide6 import QtWidgets
import utils


class CharSearcher:
    def run(self) -> int | None:
        if not (character := self.get_input()):
            return
        if not (jineima := self.get_jineima(character)):
            return
        qu, wei = utils.jineima_to_quweima(jineima)
        return utils.quweima_to_charid(qu, wei)
    
    def get_input(self) -> str | None:
        result: tuple[str, bool] = QtWidgets.QInputDialog.getText(None, '按字符搜索', '请输入要搜索的字符：')
        user_input, ok = result
        if not ok:
            return
        if len(user_input) == 0:
            QtWidgets.QMessageBox.warning(None, '搜索错误', '您没有输入任何字符')
            return
        return user_input[0]
    
    def get_jineima(self, character: str) -> bytes | None:
        try:
            jineima = utils.char_to_jineima(character, errors = 'strict')
        except UnicodeEncodeError:  # the character has no gb2312 coding
            QtWidgets.QMessageBox.warning(None, '搜索错误', '您输入的字符没有G2312编码')
            return
        if len(jineima) == 1:  # half width characters
            jineima = bytes([0xA0, 0x80 + int.from_bytes(jineima)])
        return jineima

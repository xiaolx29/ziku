from typing import Final
from PySide6 import QtWidgets

QU_COUNT: Final = 94

class QuControlSpinbox(QtWidgets.QSpinBox):
    def __init__(self):
        super().__init__()

        # qu 1 to 94
        self.setMinimum(1)
        self.setMaximum(QU_COUNT)

        # set disabled until a font file is imported
        self.setEnabled(False)

        # set format to '第？区'
        self.setPrefix('第 ')
        self.setSuffix(f'/{QU_COUNT} 区')
    
    def on_file_import(self) -> None:
        self.setEnabled(True)
        self.setValue(1)
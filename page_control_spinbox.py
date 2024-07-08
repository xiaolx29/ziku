from PySide6 import QtWidgets

class PageControlSpinbox(QtWidgets.QSpinBox):
    def __init__(self):
        super().__init__()

        # page 1 on default
        self.setMinimum(1)

        # set disabled until a font file is imported
        self.setEnabled(False)

        # set format to '第？页'
        self.setPrefix('第 ')
        self.setSuffix(' 页')
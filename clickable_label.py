from PySide6 import QtCore, QtWidgets, QtGui

class ClickableLabel(QtWidgets.QLabel):
    single_clicked = QtCore.Signal(QtCore.QPoint)
    double_clicked = QtCore.Signal(QtCore.QPoint)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        # if left mouse button clicked
        if event.button() == QtCore.Qt.LeftButton:
            # emit a signal and pass mouse position
            self.single_clicked.emit(event.position().toPoint())
    
    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        # if left mouse button double clicked
        if event.button() == QtCore.Qt.LeftButton:
            pass
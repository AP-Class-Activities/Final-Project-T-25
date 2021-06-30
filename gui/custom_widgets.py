from PyQt5.QtWidgets import QLabel, QMenu
from PyQt5.QtCore import pyqtSignal


class QClickLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        QLabel.mousePressEvent(self, event)


class ClickMenu(QMenu):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        QLabel.mousePressEvent(self, event)


from PyQt5.QtWidgets import (QApplication, QLabel, QVBoxLayout, QPushButton,
                             QWidget, QFormLayout, QDialog, QDialogButtonBox,
                             QLineEdit, QMainWindow, QToolBar, QStatusBar,
                             QHBoxLayout, QGroupBox, QGridLayout, QFrame,
                             QMenuBar, QAction, QScrollArea)
from PyQt5.QtGui import QPixmap, QFont, QTextDocument
from PyQt5.QtCore import QRect, Qt
from functools import partial
from gui.custom_widgets import QClickLabel
from core import explorer
from core import constants
import os


class HistoryItemVIew(QWidget):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.items = items
        self.setLayout(self._create_items_layout())
        self.setStyleSheet('border: 1px solid red; background-color: white;')

    def _create_items_layout(self):
        vlayout = QVBoxLayout()

        for product_id, data in self.items.items():
            hlayout = QHBoxLayout()
            image = explorer.get_image(product_id, constants.product_image_filepath())
            label = QLabel()
            pixmap = QPixmap(image)
            label.setPixmap(pixmap)
            hlayout.addWidget(label)
            hlayout.addWidget(QLabel(str(product_id)))
            hlayout.addWidget(QLabel(str(data[0])))
            hlayout.addWidget(QLabel(str(data[1])))
            hlayout.addWidget(QLabel(str(data[2])))
            vlayout.addLayout(hlayout)

        return vlayout

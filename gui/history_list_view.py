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


class HistoryListView(QWidget):
    def __init__(self, user_id, method, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.method = method
        self.setLayout(self._create_history_list())
        self.setStyleSheet('border: 1px solid red; background-color: white;')

    def _create_history_list(self):
        vlayout = QVBoxLayout()
        history_list = explorer.get_all(os.path.join(constants.history_filepath(), str(self.user_id)))

        for i in range(len(history_list)):
            label = QPushButton('Order Number ' + str(i + 1))
            label.setMaximumHeight(128)
            label.clicked.connect(partial(self.method, history_list[i]['items']))
            vlayout.addWidget(label)

        return vlayout

from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QLabel, QPushButton,
                             QWidget, QHBoxLayout)


class WalletView(QWidget):
    def __init__(self, user, method, usertype, parent=None):
        super().__init__(parent)
        self.user = user
        self.add_credits = method
        self.usertype = usertype
        self.credits = 100
        self.setLayout(self._create_wallet_part())
        self.setStyleSheet('border: 1px solid green; background-color: white;')

    def _create_wallet_part(self):
        hlayout = QHBoxLayout()
        counter_label = QLabel('100')
        minus_button = QPushButton('-')
        minus_button.clicked.connect(partial(self._reduce, counter_label))
        plus_button = QPushButton('+')
        plus_button.clicked.connect(partial(self._increase, counter_label))
        if self.usertype == 'customer':
            add_button = QPushButton('Charge Wallet')
            add_button.clicked.connect(self.charge_wallet)
        elif self.usertype == 'supplier':
            add_button = QPushButton('Withdraw')
            add_button.clicked.connect(self.withdraw)
        for widget in [counter_label, minus_button, plus_button]:
            widget.setMaximumHeight(200)
            widget.setStyleSheet('background-color: limegreen; font-size: 24px; font-weight: bold;')
        counter_label.setAlignment(Qt.AlignCenter)
        add_button.setMaximumHeight(200)
        add_button.setStyleSheet('QPushButton::hover {background-color: green;} QPushButton {background-color: limegreen; font-weight: bold; font-size: 28px;}')
        hlayout.addWidget(minus_button)
        hlayout.addWidget(counter_label)
        hlayout.addWidget(plus_button)
        hlayout.addWidget(add_button)
        return hlayout

    def charge_wallet(self):
        self.add_credits(self.credits)

    def withdraw(self):
        self.add_credits(self.credits)

    def _reduce(self, label):
        if int(label.text()) <= 100:
            return
        label.setText(str(int(label.text()) - 100))
        self.credits -= 100

    def _increase(self, label):
        if self.usertype == 'supplier':
            if int(label.text()) >= self.user.wallet:
                return
        if int(label.text()) >= 100000:
            return
        label.setText(str(int(label.text()) + 100))
        self.credits += 100

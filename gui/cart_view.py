from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QPushButton,
                             QWidget, QLineEdit, QHBoxLayout, QGridLayout, QFrame)

from core import explorer, constants


class CartView(QWidget):
    def __init__(self, cart, checkout_method, parent=None):
        # cart = [[product_id, quantity, price]]
        super().__init__(parent)
        if not cart:
            self.cart = []
        else:
            self.cart = cart
        self.checkout_method = checkout_method
        main_layout = QGridLayout()
        main_layout.addWidget(self._create_item_listing_part(), 0, 0, 1, 2)
        main_layout.addLayout(self._create_coupon_part(), 1, 0)
        main_layout.addWidget(self._create_order_details_part(), 1, 1)
        main_layout.setColumnStretch(0, 5)
        main_layout.setColumnStretch(1, 5)
        self.setLayout(main_layout)
        # self.setStyleSheet('border: 1px solid red; background-color: white;')

    def _create_item_listing_part(self):
        vlayout = QVBoxLayout()
        label1 = QLabel('image')
        label2 = QLabel('name')
        label3 = QLabel('unit price')
        label4 = QLabel('Quantity')
        label5 = QLabel('total price')

        for i in [label1, label2, label3, label4, label5]:
            i.setAlignment(Qt.AlignCenter)
            i.setMaximumHeight(128)
            i.setStyleSheet('font-weight: bold; font-size: 18px; background-color: #b3b3b3;')

        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine)
        vlayout.addWidget(separator1)
        hlayout = QHBoxLayout()
        hlayout.addWidget(label1)
        hlayout.addWidget(label2)
        hlayout.addWidget(label3)
        hlayout.addWidget(label4)
        hlayout.addWidget(label5)
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(separator2)
        if self.cart.items:
            for k, item in self.cart.items.items():
                product = explorer.search(int(k), constants.product_data_filepath())
                image = explorer.get_image(product['id'], constants.product_image_filepath())
                hlayout = QHBoxLayout()
                image_label = QLabel()
                pixmap = QPixmap(image)
                image_label.setPixmap(pixmap)
                hlayout.addWidget(image_label)
                hlayout.addWidget(QLabel(str(product['name'])))
                hlayout.addWidget(QLabel(str(product['price'])))
                hlayout.addWidget(QLabel(str(item[0])))
                total_price = int(product['price']) * int(item[0])
                hlayout.addWidget(QLabel(str(total_price)))
                vlayout.addLayout(hlayout)
        else:
            label = QLabel('Your Items Appear Here')
            label.setStyleSheet('font-weight: bold; font-size: 28px;')
            label.setAlignment(Qt.AlignCenter)
            vlayout.addWidget(label)
        vlayout.setContentsMargins(0, 0, 0, 10)
        widget = QWidget()
        widget.setLayout(vlayout)
        widget.setStyleSheet('background-color: #d9d9d9;')
        return widget

    def _create_coupon_part(self):
        header = QLabel('COUPON CODE')
        header.setAlignment(Qt.AlignCenter)

        enter_coupon = QLineEdit()
        enter_coupon.setPlaceholderText('Enter your coupon code here')

        enter_button = QPushButton('Checkout')

        vlayout = QVBoxLayout()
        vlayout.addWidget(header)
        vlayout.addWidget(enter_coupon)
        vlayout.addWidget(enter_button)

        return vlayout

    def _create_order_details_part(self):
        header = QLabel('ORDER DETAILS')
        header.setStyleSheet('background-color: #b3b3b3;')
        header.setAlignment(Qt.AlignCenter)

        subtotal = 0
        items = self.cart.items
        for _, v in items.items():
            subtotal += int(v[1]) * int(v[0])
        subtotal = QLabel(str(subtotal))
        coupon_off = QLabel('$800')
        total = QLabel('$500')
        checkout_button = QPushButton('Checkout')
        checkout_button.setStyleSheet('QPushButton::hover {background-color: limegreen;}'
                                      '{background-color: #b3b3b3; background-color:hover: red;}')
        checkout_button.setMinimumHeight(64)
        checkout_button.clicked.connect(self.checkout)

        vlayout = QGridLayout()
        vlayout.addWidget(header, 0, 0, 1, 2)
        vlayout.addWidget(QLabel('SUBTOTAL'), 1, 0)
        vlayout.addWidget(subtotal, 1, 1)
        vlayout.addWidget(QLabel('COUPON OFF'), 2, 0)
        vlayout.addWidget(coupon_off, 2, 1)
        vlayout.addWidget(QLabel('TOTAL'), 3, 0)
        vlayout.addWidget(total, 3, 1)
        vlayout.addWidget(checkout_button, 4, 0, 1, 2)
        widget = QWidget()
        widget.setLayout(vlayout)
        widget.setStyleSheet('border: 1px solid gray; background-color: white; background-color: #d9d9d9;')
        return widget

    def checkout(self):
        self.checkout_method()

from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QWidget, QHBoxLayout, QGridLayout)

from core import explorer, constants
from gui.custom_widgets import QClickLabel


class ItemCategory(QWidget):
    def __init__(self, category, method, parent=None):
        super().__init__(parent)
        self.category = category
        self.method = method

        self.main_layout = QVBoxLayout()
        self._get_product()
        self.setLayout(self.main_layout)
        self.setStyleSheet('border: 1px solid red; background-color: white;')

    def _get_product(self):
        products_list = explorer.find_all('category', self.category, constants.product_data_filepath())
        # for product in products_list:
        #     if not product['is_approved']:
        #         products_list.remove(product)
        image_list = []
        for product in products_list:
            image_list.append(explorer.get_image(product['id'], constants.product_image_filepath()))

        count = 0
        for product in products_list:
            layout = QGridLayout()

            # Image
            pixmap = QPixmap(image_list[count])
            image = QLabel()
            image.setPixmap(pixmap)
            image.setAlignment(Qt.AlignCenter)
            image.setWordWrap(True)

            # Name
            name = QLabel(product['name'])
            name.setAlignment(Qt.AlignCenter)
            name.setStyleSheet('font-weight: bold; font-size: 18px;')
            name.setWordWrap(True)

            # Price
            price = QLabel(str(product['price']))
            price.setStyleSheet('font-size: 14px; font-weight: bold;')
            price.setAlignment(Qt.AlignCenter)
            price.setWordWrap(True)

            # Description
            text = 'In publishing and graphic design, Lorem ipsum is a placeholder text commonly' \
                   ' used to demonstrate the visual form of a document or a typeface without relying' \
                   ' on meaningful content. Lorem ipsum may be used as a placeholder before final copy is available.'
            desc = QLabel(product['description'])
            desc.setWordWrap(True)

            # Name and price layout
            mini_layout = QHBoxLayout()
            mini_layout.addWidget(name)
            mini_layout.addWidget(price)

            layout.setRowStretch(0, 6)
            layout.setRowStretch(1, 2)
            layout.setRowStretch(2, 2)
            layout.addWidget(image, 0, 0)
            layout.addLayout(mini_layout, 1, 0)
            layout.addWidget(desc, 2, 0)
            label = QClickLabel(self)
            label.setLayout(layout)
            label.setObjectName('item-label')
            label.setStyleSheet(
                'QLabel {border: 1px solid red; background-color: white;} QClickLabel::hover {background-color: #cfffd3;}')
            label.setMaximumSize(640, 640)
            label.clicked.connect(
                partial(self.change_to_product, product['id'], product['supplier_id'], image_list[count], name.text(), price.text(), desc.text()))
            self.main_layout.addWidget(label)
            count += 1

    def change_to_product(self, product_id, supplier_id, image, name, price, desc):
        self.method(product_id, supplier_id, image, name, price, desc)

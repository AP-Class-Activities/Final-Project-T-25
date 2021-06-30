import os
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QPushButton,
                             QWidget, QLineEdit, QHBoxLayout, QMessageBox)

from core import explorer, constants
from core.comments import Comment


class ProductView(QWidget):
    def __init__(self, add_to_cart, product_id=None, supplier_id=None, image=None, name=None, price=None, desc=None, user=None, usertype=None, parent=None):
        super().__init__(parent)
        self.product_id = product_id
        self.supplier_id = supplier_id
        self.image = image
        self.name = name
        self.price = price
        self.desc = desc
        self.user = user
        self.usertype = usertype
        self.add_to_cart = add_to_cart
        self.comments = explorer.get_all(os.path.join(constants.product_comments_filepath(), str(self.product_id)))
        self.product_dict = explorer.search(self.product_id, constants.product_data_filepath())
        self.quantity = 1

        first_row = QHBoxLayout()
        first_row.addLayout(self._create_product_ui())
        first_row.addLayout(self._create_cart_ui())
        first_row.setStretch(0, 85)
        first_row.setStretch(1, 15)

        main_vlayout = QVBoxLayout()
        main_vlayout.addLayout(first_row)
        main_vlayout.addLayout(self._create_comments_ui())
        main_vlayout.addLayout(self._create_post_comment_ui())

        self.setLayout(main_vlayout)
        self.setStyleSheet('border: 1px solid red; background-color: white;')

    def _create_product_ui(self):
        pixmap = QPixmap(self.image)
        image = QLabel()
        image.setPixmap(pixmap)
        image.setAlignment(Qt.AlignCenter)
        image.setMinimumHeight(500)

        vlayout = QVBoxLayout()

        votes = list(map(int, self.product_dict['rating'].split('-')))
        try:
            rating = (5 * votes[4] + 4 * votes[3] + 3 * votes[2] + 2 * votes[1] + 1 * votes[0]) / sum(votes)
        except ZeroDivisionError:
            rating = 0

        # Name and Rating
        name_and_rating = QHBoxLayout()
        name = QLabel(self.name)
        rating = QLabel(str(rating))
        name_and_rating.addWidget(name)
        name_and_rating.addWidget(rating)
        name_and_rating.setStretch(0, 8)
        name_and_rating.setStretch(1, 2)

        price = QLabel(self.price)
        desc = QLabel(self.desc)
        desc.setWordWrap(True)
        vlayout.addLayout(name_and_rating)
        vlayout.addWidget(price)
        vlayout.addWidget(desc)

        hlayout = QHBoxLayout()
        hlayout.addWidget(image)
        hlayout.addLayout(vlayout)
        hlayout.setStretch(0, 30)
        hlayout.setStretch(1, 70)
        return hlayout

    def _create_cart_ui(self):
        vlayout = QVBoxLayout()
        total_price = QLabel('$600')

        # Counter
        counter_layout = QHBoxLayout()
        counter_label = QLabel('1')
        minus_button = QPushButton('-')
        minus_button.clicked.connect(partial(self._reduce, counter_label))
        plus_button = QPushButton('+')
        plus_button.clicked.connect(partial(self._increase, counter_label))
        if self.product_dict['count'] == 0:
            counter_label.setText('Unavailable')
            minus_button.setDisabled(True)
            plus_button.setDisabled(True)
        counter_layout.addWidget(minus_button)
        counter_layout.addWidget(counter_label)
        counter_layout.addWidget(plus_button)

        # Add button
        add_button = QPushButton('Add To Cart')
        add_button.clicked.connect(self.call_add_to_cart)
        if self.usertype != 'customer' or self.product_dict['count'] == 0:
            add_button.setDisabled(True)

        vlayout.addWidget(total_price)
        vlayout.addLayout(counter_layout)
        vlayout.addWidget(add_button)
        return vlayout

    def _reduce(self, label):
        if int(label.text()) <= 1:
            return
        label.setText(str(int(label.text()) - 1))
        self.quantity = label.text()

    def _increase(self, label):
        if int(label.text()) >= 10 or int(label.text()) >= self.product_dict['count']:
            return
        label.setText(str(int(label.text()) + 1))
        self.quantity = label.text()

    def call_add_to_cart(self):
        self.add_to_cart(self.product_id, int(self.quantity), self.price, self.supplier_id)

    def _create_comments_ui(self):
        hlayout = QVBoxLayout()
        for comment in self.comments:
            comment_label = QLabel(comment['text'])
            comment_label.setMinimumHeight(160)
            comment_label.setWordWrap(True)
            rating_label = QLabel(str(comment['rating']))
            hlayout.addWidget(comment_label)
            hlayout.addWidget(rating_label)
        return hlayout

    def _create_post_comment_ui(self):
        hlayout = QHBoxLayout()
        self.comment_text = QLineEdit()
        self.comment_text.setPlaceholderText('Tell the others what you feel about this product ...')
        self.comment_text.setMinimumHeight(160)
        self.comment_text.setAlignment(Qt.AlignTop)
        post = QPushButton('Post comment')
        post.clicked.connect(self.post_comment)
        post.setMinimumHeight(160)
        if self.usertype != 'customer':
            post.setDisabled(True)
        for comment in self.comments:
            if comment['user_id'] == self.user.id:
                post.setDisabled(True)
        hlayout.addWidget(self.comment_text)
        hlayout.addWidget(post)
        return hlayout

    def post_comment(self):
        Comment(self.comment_text.text(), 5, self.user.id, self.product_id, True)
        product = explorer.search(self.product_id, constants.product_data_filepath())
        votes = list(map(int, product['rating'].split('-')))
        votes[5-1] += 1
        votes = [str(i) for i in votes]
        rating = '-'.join(votes)
        product['rating'] = rating
        explorer.overwrite(constants.product_data_filepath(), product)
        QMessageBox.about(self, 'Success', 'Comment posted successfully')
        self.sender().setDisabled(True)

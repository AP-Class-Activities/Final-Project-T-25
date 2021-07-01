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
        self.user_rating = 5
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
        self.setStyleSheet('border: 1px solid green; background-color: white;')

    def _create_product_ui(self):
        pixmap = QPixmap(self.image)
        pixmap2 = pixmap.scaledToHeight(400)
        image = QLabel()
        image.setPixmap(pixmap2)
        image.setAlignment(Qt.AlignCenter)
        image.setMaximumHeight(500)

        vlayout = QVBoxLayout()

        votes = list(map(int, self.product_dict['rating'].split('-')))
        print(self.product_dict['rating'])
        print(votes)
        try:
            rating = (5 * votes[4] + 4 * votes[3] + 3 * votes[2] + 2 * votes[1] + 1 * votes[0]) / sum(votes)
        except ZeroDivisionError:
            rating = 0

        # Name and Rating
        name_and_rating = QHBoxLayout()
        name = QLabel(self.name)
        name.setMaximumHeight(200)
        rating = QLabel(str(rating) + ' Stars')
        rating.setMaximumHeight(200)
        rating.setAlignment(Qt.AlignCenter)
        name_and_rating.addWidget(name)
        name_and_rating.addWidget(rating)
        name_and_rating.setStretch(0, 8)
        name_and_rating.setStretch(1, 2)

        price = QLabel(str(self.price))
        price.setMaximumHeight(100)
        desc = QLabel(str(self.desc))
        desc.setWordWrap(True)
        desc.setMaximumHeight(200)

        for widget in [name, rating, price, desc]:
            widget.setStyleSheet('background-color: #d9ffdf; font-size: 24px; font-weight: bold;')

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
        for widget in [minus_button, plus_button, counter_label]:
            widget.setMinimumHeight(100)
            widget.setStyleSheet('font-size: 18px; background-color: #baffc6;')
        counter_label.setAlignment(Qt.AlignCenter)
        counter_layout.addWidget(minus_button)
        counter_layout.addWidget(counter_label)
        counter_layout.addWidget(plus_button)

        # Add button
        add_button = QPushButton('Add To Cart')
        add_button.setMinimumHeight(64)
        add_button.clicked.connect(self.call_add_to_cart)
        add_button.setStyleSheet('QPushButton::hover {background-color: green;} QPushButton {background-color: limegreen; font-weight: bold; font-size: 28px;}')
        if self.usertype != 'customer' or self.product_dict['count'] == 0:
            add_button.setDisabled(True)

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
        hlayout = QHBoxLayout()
        for comment in self.comments:
            comment_label = QLabel(comment['text'])
            comment_label.setMinimumHeight(160)
            comment_label.setWordWrap(True)
            rating_label = QLabel(str(comment['rating']) + ' Stars')
            rating_label.setAlignment(Qt.AlignCenter)
            comment_label.setStyleSheet('background-color: #edfff0; font-size: 18px;')
            rating_label.setStyleSheet('background-color: #edfff0; font-size: 26px;')
            hlayout.addWidget(comment_label)
            hlayout.addWidget(rating_label)
            hlayout.setStretch(0, 9)
            hlayout.setStretch(1, 1)
        return hlayout

    def _create_post_comment_ui(self):
        hlayout = QHBoxLayout()
        self.comment_text = QLineEdit()
        self.comment_text.setPlaceholderText('Tell the others what you feel about this product ...')
        self.comment_text.setMinimumHeight(160)
        self.comment_text.setAlignment(Qt.AlignTop)
        post = QPushButton('Post comment')
        post.clicked.connect(self.post_comment)
        post.setMinimumHeight(36)
        if self.usertype != 'customer':
            post.setDisabled(True)
        for comment in self.comments:
            if comment['user_id'] == self.user.id:
                post.setDisabled(True)

        rater = QVBoxLayout()
        counter_label = QLabel('5')
        counter_label.setAlignment(Qt.AlignCenter)
        counter_label.setMaximumHeight(36)
        minus_button = QPushButton('-')
        minus_button.clicked.connect(partial(self._reduce_rating, counter_label))
        plus_button = QPushButton('+')
        plus_button.clicked.connect(partial(self._increase_rating, counter_label))
        rater.addWidget(plus_button)
        rater.addWidget(counter_label)
        rater.addWidget(minus_button)
        rater.addWidget(post)

        hlayout.addWidget(self.comment_text)
        hlayout.addLayout(rater)

        return hlayout

    def post_comment(self):
        Comment(self.comment_text.text(), int(self.user_rating), self.user.id, self.product_id, True)
        product = explorer.search(self.product_id, constants.product_data_filepath())
        votes = list(map(int, product['rating'].split('-')))
        votes[int(self.user_rating)-1] += 1
        votes = [str(i) for i in votes]
        rating = '-'.join(votes)
        product['rating'] = rating
        explorer.overwrite(constants.product_data_filepath(), product)
        QMessageBox.about(self, 'Success', 'Comment posted successfully')
        self.sender().setDisabled(True)

    def _reduce_rating(self, label):
        if int(label.text()) <= 1:
            return
        label.setText(str(int(label.text()) - 1))
        self.user_rating = label.text()

    def _increase_rating(self, label):
        if int(label.text()) >= 5:
            return
        label.setText(str(int(label.text()) + 1))
        self.user_rating = label.text()

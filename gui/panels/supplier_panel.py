from PyQt5.QtWidgets import (QApplication, QLabel, QVBoxLayout, QPushButton,
                             QWidget, QFormLayout, QDialog, QDialogButtonBox,
                             QLineEdit, QMainWindow, QToolBar, QStatusBar,
                             QHBoxLayout, QGroupBox, QGridLayout, QFrame,
                             QMenuBar, QAction, QScrollArea, QTextEdit,
                             QTabWidget, QComboBox, QFileDialog, QMessageBox)
from PyQt5.QtGui import QPixmap, QFont, QTextDocument
from PyQt5.QtCore import QRect, Qt
from functools import partial
from core import explorer, constants
from core.products import Product
import os


class SupplierPanel(QTabWidget):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.orders = explorer.get_all(os.path.join(constants.supplier_logs_filepath(), str(self.user.id)))
        self.overview_tab = QWidget()
        self.new_product_tab = QWidget()
        self.orders_tab = QWidget()
        self.my_products = QWidget()

        self.addTab(self.overview_tab, "Tab 1")
        self.addTab(self.new_product_tab, "Tab 2")
        self.addTab(self.orders_tab, "Tab 3")
        self.addTab(self.my_products, "Tab 4")

        self.overview_tab.setLayout(self._create_overview())
        self.setTabText(0, 'Overview')

        self.new_product_tab.setLayout(self._create_new_product())
        self.setTabText(1, 'Add a Product')

        self.orders_tab.setLayout(self._create_orders_part())
        self.setTabText(2, 'Orders')

        self.my_products.setLayout(self._create_my_products())
        self.setTabText(3, 'My Products')

        self.setStyleSheet('border: 1px solid red; background-color: white;')

    def _create_overview(self):
        layout = QVBoxLayout()
        layout.addLayout(self._create_top_part())
        layout.addLayout(self._create_details_part())
        layout.addLayout(self._create_recent_details())
        return layout

    def _create_top_part(self):
        panel_name = QLabel('Supplier Panel')

        # buttons
        button_layout = QHBoxLayout()

        hlayout = QHBoxLayout()
        hlayout.addWidget(panel_name)
        hlayout.addLayout(button_layout)
        hlayout.setStretch(0, 8)
        hlayout.setStretch(1, 2)
        return hlayout

    def _create_details_part(self):
        left_layout = QGridLayout()
        hlayout = QHBoxLayout()

        total_revenue = 0
        sold_items = 0
        unique_product_ids = set()
        for order in self.orders:
            for item in order['items']:
                total_revenue += int(item[0]) * int(item[1])
                sold_items += item[0]
                unique_product_ids.add(item[2])

        label1 = QLabel('Overall State')
        label2 = QLabel(f'Total Revenue\n${total_revenue}')
        label3 = QLabel(f'Total Orders\n{len(self.orders)}')
        label4 = QLabel(f'Items Sold\n{sold_items}')
        label5 = QLabel(f'Unique Items Sold\n{len(unique_product_ids)}')

        left_layout.addWidget(label1, 0, 0, 1, 4)
        left_layout.addWidget(label2, 1, 0)
        left_layout.addWidget(label3, 1, 1)
        left_layout.addWidget(label4, 1, 2)
        left_layout.addWidget(label5, 1, 3)

        hlayout.addLayout(left_layout)
        hlayout.setContentsMargins(0, 24, 0, 24)
        return hlayout

    def _create_recent_details(self):
        vlayout = QVBoxLayout()
        vlayout.addWidget(QLabel('RECENT ORDERS'))

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel('Names'))
        hlayout.addWidget(QLabel('Order Date'))
        hlayout.addWidget(QLabel('Delivered'))
        vlayout.addLayout(hlayout)

        for order in self.orders[-5:]:
            product = []
            for data in order['items']:
                product.append(explorer.search(data[2], constants.product_data_filepath())['name'])

            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel(', '.join(product)))
            hlayout.addWidget(QLabel(str(order['time'])))
            hlayout.addWidget(QLabel(str(order['is_delivered'])))
            vlayout.addLayout(hlayout)

        return vlayout

    def _create_new_product(self):
        category_label = QLabel('Category')
        name_label = QLabel('name')
        weight_label = QLabel('weight')
        desc_label = QLabel('description')
        price_label = QLabel('price')
        count_label = QLabel('count')
        image_button = QPushButton('Select Image')
        image_button.clicked.connect(self.open_image)

        for widget in [category_label, name_label, weight_label, desc_label, price_label, count_label]:
            widget.setMinimumHeight(96)
            widget.setStyleSheet('background-color: #e6e6e6;')

        self.image_path = None
        self.category_field = QComboBox()
        self.category_field.addItems(constants.CATEGORIES)
        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText('Enter name here')
        self.weight_field = QLineEdit()
        self.weight_field.setPlaceholderText('Enter weight here')
        self.desc_field = QLineEdit()
        self.desc_field.setPlaceholderText('Enter description here')
        self.price_field = QLineEdit()
        self.price_field.setPlaceholderText('Enter price here')
        self.count_field = QLineEdit()
        self.count_field.setPlaceholderText('Enter count here')

        for widget in [self.category_field, self.name_field, self.weight_field, self.desc_field, self.price_field, self.count_field, image_button]:
            widget.setMinimumHeight(64)
            widget.setStyleSheet('background-color: #edfff4;')

        form = QGridLayout()
        form.addWidget(category_label, 0, 0)
        form.addWidget(self.category_field, 1, 0)
        form.addWidget(name_label, 0, 1)
        form.addWidget(self.name_field, 1, 1)

        form.addWidget(weight_label, 2, 0)
        form.addWidget(self.weight_field, 3, 0)
        form.addWidget(desc_label, 2, 1)
        form.addWidget(self.desc_field, 3, 1)

        form.addWidget(price_label, 4, 0)
        form.addWidget(self.price_field, 5, 0)
        form.addWidget(count_label, 4, 1)
        form.addWidget(self.count_field, 5, 1)

        add_button = QPushButton('Add Product')
        add_button.clicked.connect(self.check_inputs)
        add_button.setMinimumHeight(96)
        add_button.setStyleSheet('QPushButton::hover {background-color: limegreen;} QPushButton {background-color: #b3b3b3;} ')
        form.addWidget(image_button, 6, 0, 1, 1)
        form.addWidget(add_button, 7, 0, 1, 2)
        form.setAlignment(Qt.AlignCenter)
        return form

    def _create_orders_part(self):
        vlayout = QVBoxLayout()

        orders_list = explorer.get_all(os.path.join(constants.supplier_logs_filepath(), str(self.user.id)))
        for order in orders_list:
            for item in order['items']:
                hlayout = QHBoxLayout()
                product = explorer.search(int(item[2]), constants.product_data_filepath())
                name = QLabel(str(product['name']))
                quantity = QLabel(str(item[0]))
                price = QLabel(str(item[1]))
                approve = QPushButton('Approve')
                approve.clicked.connect(partial(self.approve_delivery, order['id']))
                if order['is_delivered']:
                    approve.setText('Order Delivered')
                    approve.setDisabled(True)
                for widget in [name, quantity, price, approve]:
                    widget.setMinimumHeight(64)
                    widget.setStyleSheet('background-color: #e6e6e6;')
                approve.setStyleSheet('QPushButton::hover {background-color: limegreen;} {background-color: #cccccc;}')
                hlayout.addWidget(name)
                hlayout.addWidget(quantity)
                hlayout.addWidget(price)
                hlayout.addWidget(approve)
                hlayout.setAlignment(Qt.AlignTop)
                vlayout.addLayout(hlayout)
        return vlayout

    def approve_delivery(self, log_id):
        path = os.path.join(constants.supplier_logs_filepath(), str(self.user.id))
        log = explorer.search(log_id, path)
        log['is_delivered'] = True
        explorer.overwrite(path, log)
        self.sender().setText('Order Delivered!')
        self.sender().setDisabled(True)
        QMessageBox.about(self, 'Success', 'Order Delivered!')

    def open_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select Image', 'C:\\Desktop\\', 'Images (*.png *.jpg *.jpeg)')
        self.image_path = filename

    def check_inputs(self):
        if self.category_field and self.name_field and self.weight_field and self.desc_field\
                and self.price_field and self.count_field and self.image_path:
            self._create_product()
        else:
            QMessageBox.about(self, 'Error', 'Please fill all of the fields')

    def _create_product(self):
        product = Product(str(self.category_field.currentText()), self.name_field.text(), int(self.weight_field.text()),
                          self.desc_field.text(), int(self.price_field.text()), int(self.count_field.text()), int(self.user.id))
        explorer.save_image(constants.product_image_filepath(), self.image_path, str(product.id))
        QMessageBox.about(self, 'Success', 'Product added successfully')

    def _create_my_products(self):
        products = explorer.find_all('supplier_id', self.user.id, constants.product_data_filepath())
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        image = QLabel('Image')
        name = QLabel('Name')
        price = QLabel('Price')
        count = QLabel('Count')
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet('background-color: black;')
        for widget in [image, name, price, count]:
            widget.setAlignment(Qt.AlignCenter)
            widget.setMaximumHeight(256)
            widget.setStyleSheet('background-color: #a3a3a3;')
            hlayout.addWidget(widget)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(line)

        for product in products:
            hlayout = QHBoxLayout()
            image = explorer.get_image(product['id'], constants.product_image_filepath())
            pixmap = QPixmap(image)
            image = QLabel()
            image.setPixmap(pixmap)

            name = QLabel(str(product['name']))
            price = QLabel(str(product['price']))
            count = QLabel(str(product['count']))

            for widget in [name, price, count]:
                widget.setAlignment(Qt.AlignCenter)
                widget.setMaximumHeight(256)
                widget.setStyleSheet('background-color: #d9d7d7;')
            image.setMaximumHeight(256)
            image.setAlignment(Qt.AlignCenter)

            hlayout.addWidget(image)
            hlayout.addWidget(name)
            hlayout.addWidget(price)
            hlayout.addWidget(count)
            vlayout.addLayout(hlayout)
        return vlayout

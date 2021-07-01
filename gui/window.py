from PyQt5.QtWidgets import (QApplication, QLabel, QVBoxLayout, QPushButton,
                             QWidget, QMainWindow, QHBoxLayout, QGroupBox,
                             QGridLayout, QMenuBar, QAction, QScrollArea,
                             QStackedWidget, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from functools import partial
from gui.product_view import ProductView
from gui.cart_view import CartView
from gui.custom_widgets import QClickLabel
from gui.auth.login_views import CustomerLoginView, SupplierLoginView, OperatorLoginView
from gui.auth.register_views import CustomerRegisterView, SupplierRegisterView, OperatorRegisterView
from gui.category_view import ItemCategory
from gui.panels.supplier_panel import SupplierPanel
from gui.panels.operator_panel import OperatorPanel
from gui.history_list_view import HistoryListView
from gui.history_item_view import HistoryItemVIew
from gui.wallet_view import WalletView
from core import explorer, constants
from core.users import Customer, Supplier, Operator
from core.products import Product
from core.cart import Cart
from core.history import History
from core.supplier_logs import SupplierLog
import sys
import random


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Online Shop')

        self.main_layout = QVBoxLayout()
        self.central_widget = QStackedWidget()
        self._cart = None
        self._user = None
        self._usertype = None
        self.get_user()

        # item row
        self.first_item_row = QGroupBox('Products')
        self.first_item_row.setObjectName('first_row')
        self.second_item_row = QGroupBox('Products')
        self.second_item_row.setObjectName('second_row')
        self.first_item_row.setLayout(self._create_product_row())
        self.second_item_row.setLayout(self._create_product_row())

        # setting main layout
        button_layout = self._create_top_buttons()
        self.main_layout.addLayout(button_layout)
        self.main_layout.addWidget(self.first_item_row)
        self.main_layout.addWidget(self.second_item_row)
        self.main_layout.setSpacing(40)
        # self.setLayout(self.main_layout)

        # central widget and layouts
        self._create_menubar()
        self.check_login()
        self.check_visibility()
        self.main_widget = QWidget(self)
        self.main_widget.setLayout(self.main_layout)
        self.central_widget.addWidget(self.main_widget)
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.central_widget)
        self.setCentralWidget(self.scroll)
        self.setObjectName('main_window')
        self.setStyleSheet('QMainWindow#main_window {background-color: #d1ffdc;}')

    def check_menubar(self):
        if self.sender():
            for action in self.menuBar().actions():
                if action == self.sender():
                    action.setDisabled(True)
                else:
                    action.setDisabled(False)

    def check_visibility(self):
        menubar_actions = self.menuBar().actions()
        if self._usertype == 'customer':
            for action in menubar_actions:
                if action.objectName() == 'panel_action':
                    action.setVisible(False)
                elif action.objectName() == 'cart_action' or action.objectName() == 'history_action'\
                        or action.objectName() == 'wallet_action':
                    action.setVisible(True)
        elif self._usertype == 'supplier' or self._usertype == 'operator':
            for action in menubar_actions:
                if action.objectName() == 'cart_action' or action.objectName() == 'history_action'\
                        or action.objectName() == 'wallet_action':
                    action.setVisible(False)
                elif action.objectName() == 'panel_action':
                    action.setVisible(True)
        else:
            for action in menubar_actions:
                if action.objectName() == 'cart_action' or action.objectName() == 'panel_action'\
                        or action.objectName() == 'history_action' or action.objectName() == 'wallet_action':
                    action.setVisible(False)
        if self._usertype == 'supplier':
            for action in menubar_actions:
                if action.objectName() == 'wallet_action':
                    action.setVisible(True)

    def check_login(self):
        menubar_actions = self.menuBar().actions()
        if self._user:
            for action in menubar_actions:
                if action.objectName() == 'register_action' or action.objectName() == 'login_action':
                    action.setVisible(False)
                elif action.objectName() == 'logout_action':
                    action.setVisible(True)
        else:
            for action in menubar_actions:
                if action.objectName() == 'logout_action':
                    action.setVisible(False)
                elif action.objectName() == 'register_action' or action.objectName() == 'login_action':
                    action.setVisible(True)

    @staticmethod
    def build_user(user_dict):

        if user_dict['type'] == 'customer':
            user_obj = Customer(user_dict['phone'], user_dict['email'], user_dict['password'], False)
            user_obj.wallet = user_dict['wallet']
            user_obj.id = user_dict['id']
            user_obj.is_active = user_dict['is_active']

        elif user_dict['type'] == 'supplier':
            user_obj = Supplier(user_dict['firstname'], user_dict['lastname'], user_dict['address'],
                                user_dict['phone'], user_dict['email'], user_dict['password'], False)
            user_obj.wallet = user_dict['wallet']
            user_obj.id = user_dict['id']
            user_obj.is_active = user_dict['is_active']
            user_obj.is_approved = user_dict['is_approved']
            user_obj.point = user_dict['point']

        elif user_dict['type'] == 'operator':
            user_obj = Operator(user_dict['firstname'], user_dict['lastname'], user_dict['phone'],
                                user_dict['email'], user_dict['password'], save_to_database=False)
            user_obj.id = user_dict['id']
            user_obj.is_active = user_dict['is_active']

        return user_obj

    def get_user(self):
        user_dict = explorer.get_user()
        if user_dict is None:
            return
        user_obj = self.build_user(user_dict)
        self.set_user(user_obj)
        self._usertype = user_dict['type']
        if self._usertype == 'customer':
            self.get_cart()

    def set_user(self, value, set_current=False):
        self._user = value

        if value is None:
            self._usertype = None
            self._cart = None
            explorer.flush_session()
        if set_current and value is not None:
            self._user.set_current_user()
            self.check_visibility()
            self.check_login()
            self.get_cart()

    def logout_user(self):  # ATTENTION: call self.set_user(None) after testing out
        self.set_user(None)
        self.check_visibility()
        self.check_login()

    def remove_widget_central(self):
        for i in range(self.central_widget.count()):
            if self.central_widget.widget(i) != self.main_widget:
                widget = self.central_widget.widget(i)
                widget.setParent(None)
                del widget

    def get_cart(self):
        if self._usertype == 'supplier' or self._usertype == 'operator':
            self._cart = None
            return
        temp = explorer.find('id', self._user.id, constants.cart_filepath())
        if not temp:
            self._cart = Cart(self._user.id, save_to_database=True)
        else:
            self._cart = Cart(self._user.id, temp['items'])

    def add_to_cart(self, product_id, quantity, price, supplier_id):
        QMessageBox.about(self, 'Success', 'Product added to cart successfully')
        cart = explorer.find('id', self._user.id, constants.cart_filepath())
        if not cart:
            cart = Cart(self._user.id, save_to_database=True)
        else:
            cart = Cart(cart['id'], items=cart['items'])
        cart.add_item(str(product_id), quantity, price, supplier_id)
        self._cart = cart
        self.change_to_main()

    def checkout(self):
        if self._user.wallet < self._cart.total():
            QMessageBox.about(self, 'Not Enough Credits', 'You do not have enough credits to checkout.\nplease consider charging your wallet')
            return
        if not self._cart:
            return
        History(self._user.id, self._cart.items, True)
        supplier_ids = set()
        for product_id, data in self._cart.items.items():
            supplier_ids.add(data[2])
        result = {key: [] for key in list(supplier_ids)}
        for supplier_id, data in result.items():
            for product_id, value in self._cart.items.items():
                if [value[0], value[1], product_id] not in result[value[2]]:
                    result[value[2]].append([value[0], value[1], product_id])
        supplier_logs = []
        for supplier_id, data in result.items():
            supplier_logs.append(SupplierLog(supplier_id, data, True))
        for log in supplier_logs:
            for i in log.items:
                total = int(i[0]) * int(i[1])
                supplier = explorer.search(log.supplier_id, constants.supplier_filepath())
                supplier['wallet'] += total
                explorer.overwrite(constants.supplier_filepath(), supplier)

        for product_id, data in self._cart.items.items():
            product = explorer.search(int(product_id), constants.product_data_filepath())
            product['count'] -= int(data[0])
            explorer.overwrite(constants.product_data_filepath(), product)

        self._user.wallet -= self._cart.total()
        self._cart.flush_cart()
        self._user.update()
        self.set_user(self._user, True)
        QMessageBox.about(self, 'Success', 'You have checked out successfully')
        self.change_to_main()

    def enable_all(self):
        for action in self.menuBar().actions():
            if action.objectName() == 'main_action':
                action.setDisabled(True)
            else:
                action.setDisabled(False)

    def charge_wallet(self, creditz):
        self._user.wallet += creditz
        self._user.update()
        self.set_user(self._user, True)
        self.change_to_main()

    def withdraw_wallet(self, creditz):
        self._user.wallet -= creditz
        self._user.update()
        self.set_user(self._user, True)
        self.change_to_main()

    def change_to_main(self):
        self.enable_all()
        self.remove_widget_central()
        self.central_widget.setCurrentWidget(self.main_widget)
        self.scroll.setWidget(self.central_widget)

    def change_to_wallet(self):
        if self._usertype == 'customer':
            view = WalletView(self._user, self.charge_wallet, self._usertype)
        elif self._usertype == 'supplier':
            if self._user.is_approved:
                view = WalletView(self._user, self.withdraw_wallet, self._usertype)
            else:
                QMessageBox.about(self, 'Error', 'Your Account needs to be approved by an operator first')
                return
        self.change_window(view)

    def change_to_product(self, product_id, supplier_id, image, name, price, desc):
        view = ProductView(self.add_to_cart, product_id=product_id, supplier_id=supplier_id, image=image, name=name, price=price, desc=desc, user=self._user, usertype=self._usertype)
        self.remove_widget_central()
        self.central_widget.addWidget(view)
        self.central_widget.setCurrentWidget(view)
        self.scroll.setWidget(self.central_widget)

    def change_to_category(self, category):
        view = ItemCategory(category=category, method=self.change_to_product)
        self.change_window(view)

    def change_to_cart(self):
        view = CartView(cart=self._cart, checkout_method=self.checkout)
        self.change_window(view)

    def change_to_panel(self):
        if self._usertype == 'supplier':
            if not self._user.is_approved:
                QMessageBox.about(self, 'Unidentified user', 'Your account needs to be approved by operators first')
                return
            view = SupplierPanel(self._user)
        elif self._usertype == 'operator':
            view = OperatorPanel()
        else:
            return
        self.change_window(view)

    def change_to_history(self):
        view = HistoryListView(self._user.id, self.change_to_history_item)
        self.change_window(view)

    def change_to_history_item(self, items):
        self.change_to_main()
        view = HistoryItemVIew(items)
        self.change_window(view)

    def register_user(self, user, usertype):
        self._usertype = usertype
        self.set_user(user, True)
        self.change_to_main()

    def login_user(self, user_dict, usertype):
        user_obj = self.build_user(user_dict)
        self._usertype = usertype
        self.set_user(user_obj, True)
        self.change_to_main()

    def change_to_register(self):
        self.remove_widget_central()
        layout = QHBoxLayout()
        customer_button = QPushButton('Customer')
        customer_button.clicked.connect(partial(self.change_to_customer_register))
        supplier_button = QPushButton('Supplier')
        supplier_button.clicked.connect(partial(self.change_to_supplier_register))
        operator_button = QPushButton('Operator')
        operator_button.clicked.connect(partial(self.change_to_operator_register))
        layout.addWidget(QLabel('Register As:'))
        layout.addWidget(customer_button)
        layout.addWidget(supplier_button)
        layout.addWidget(operator_button)
        widget = QWidget()
        widget.setLayout(layout)
        self.central_widget.addWidget(widget)
        self.central_widget.setCurrentWidget(widget)
        self.scroll.setWidget(self.central_widget)

    def change_to_login(self):
        self.remove_widget_central()
        layout = QHBoxLayout()
        customer_button = QPushButton('Customer')
        customer_button.clicked.connect(partial(self.change_to_customer_login))
        supplier_button = QPushButton('Supplier')
        supplier_button.clicked.connect(partial(self.change_to_supplier_login))
        operator_button = QPushButton('Operator')
        operator_button.clicked.connect(partial(self.change_to_operator_login))
        layout.addWidget(QLabel('Login As:'))
        layout.addWidget(customer_button)
        layout.addWidget(supplier_button)
        layout.addWidget(operator_button)
        widget = QWidget()
        widget.setLayout(layout)
        self.central_widget.addWidget(widget)
        self.central_widget.setCurrentWidget(widget)
        self.scroll.setWidget(self.central_widget)

    def change_to_customer_register(self):
        view = CustomerRegisterView(self.register_user)
        self.change_window(view)

    def change_to_supplier_register(self):
        view = SupplierRegisterView(self.register_user)
        self.change_window(view)

    def change_to_operator_register(self):
        view = OperatorRegisterView(self.register_user)
        self.change_window(view)

    def change_to_customer_login(self):
        view = CustomerLoginView(self.login_user)
        self.change_window(view)

    def change_to_supplier_login(self):
        view = SupplierLoginView(self.login_user)
        self.change_window(view)

    def change_to_operator_login(self):
        view = OperatorLoginView(self.login_user)
        self.change_window(view)

    def change_window(self, view):
        self.remove_widget_central()
        self.central_widget.addWidget(view)
        self.central_widget.setCurrentWidget(view)
        self.scroll.setWidget(self.central_widget)

    def _create_top_buttons(self):
        layout = QHBoxLayout()
        categories = constants.CATEGORIES
        for category in categories:
            button = QPushButton(category)
            button.setFixedSize(128, 128)
            button.clicked.connect(partial(self.change_to_category, category))
            layout.addWidget(button)
        return layout

    def _create_menubar(self):
        # creating menu bar
        menubar = QMenuBar(self)
        main_action = QAction('Online Shop', self)
        main_action.setObjectName('main_action')
        main_action.triggered.connect(self.change_to_main)
        main_action.triggered.connect(self.check_menubar)
        menubar.addAction(main_action)

        # register action
        register_action = QAction('Register', self)
        register_action.setObjectName('register_action')
        register_action.triggered.connect(self.change_to_register)
        register_action.triggered.connect(self.check_menubar)
        menubar.addAction(register_action)

        # login action
        login_action = QAction('Login', self)
        login_action.setObjectName('login_action')
        login_action.triggered.connect(self.change_to_login)
        login_action.triggered.connect(self.check_menubar)
        menubar.addAction(login_action)

        # logout action
        logout_action = QAction('Logout', self)
        logout_action.setObjectName('logout_action')
        logout_action.triggered.connect(self.logout_user)
        logout_action.triggered.connect(self.check_menubar)
        menubar.addAction(logout_action)

        # panel action
        panel_action = QAction('Panel', self)
        panel_action.setObjectName('panel_action')
        panel_action.triggered.connect(self.change_to_panel)
        panel_action.triggered.connect(self.check_menubar)
        menubar.addAction(panel_action)

        if self._user:
            register_action.setVisible(False)
            login_action.setVisible(False)
        else:
            logout_action.setVisible(False)
            panel_action.setVisible(False)

        # cart action
        cart_action = QAction('Cart', self)
        cart_action.setObjectName('cart_action')
        cart_action.triggered.connect(self.change_to_cart)
        cart_action.triggered.connect(self.check_menubar)
        menubar.addAction(cart_action)

        history_action = QAction('History', self)
        history_action.setObjectName('history_action')
        history_action.triggered.connect(self.change_to_history)
        history_action.triggered.connect(self.check_menubar)
        menubar.addAction(history_action)

        wallet_action = QAction('Wallet', self)
        wallet_action.setObjectName('wallet_action')
        wallet_action.triggered.connect(self.change_to_wallet)
        wallet_action.triggered.connect(self.check_menubar)
        menubar.addAction(wallet_action)

        # menu bar style sheet
        menubar.setStyleSheet('''
                                QMenuBar {background-color: #a4fcbb; font-weight: bold; font-size: 20px;}
                                QMenuBar::item { margin: 10px 14px 10px 14px; border-radius: 20px; padding: 6px;}
                                QMenuBar::item:selected {background-color: lime;}
                                ''')
        self.setMenuBar(menubar)

    def _next_item(self, layout):
        widgets = [layout.itemAt(i).widget() for i in range(layout.count())]
        visible_widgets = [i for i in widgets if i.isVisible()]
        prev_widget = visible_widgets[0]
        next_widget = layout.itemAt(int(visible_widgets[-1].objectName().split('-')[-1])+1).widget()
        prev_widget.setHidden(True)
        next_widget.setHidden(False)
        if next_widget == widgets[-1]:
            self.sender().setDisabled(True)
        layout.parent().itemAt(1).widget().setDisabled(False)

    def _previous_item(self, layout):
        widgets = [layout.itemAt(i).widget() for i in range(layout.count())]
        visible_widgets = [i for i in widgets if i.isVisible()]
        prev_widget = layout.itemAt(int(visible_widgets[0].objectName().split('-')[-1])-1).widget()
        next_widget = visible_widgets[-1]
        prev_widget.setHidden(False)
        next_widget.setHidden(True)
        if prev_widget == widgets[0]:
            self.sender().setDisabled(True)
        layout.parent().itemAt(2).widget().setDisabled(False)

    def _create_product_row(self):
        grid = QGridLayout()
        product_layout = QHBoxLayout()

        random_items = explorer.random_products(constants.CATEGORIES[0], 8)

        for i in range(5):  # Visible items
            widget = self._create_group(i, random_items[i])
            widget.setObjectName(f'col-{i}')
            product_layout.addWidget(widget)
        for i in range(5, 8):  # Invisible items
            widget = self._create_group(i, random_items[i])
            widget.setObjectName(f'col-{i}')
            widget.setHidden(True)
            product_layout.addWidget(widget)

        grid.addLayout(product_layout, 0, 1)
        btn1 = QPushButton('<')
        btn1.setObjectName('prev_item')
        btn1.setDisabled(True)
        btn1.setMaximumSize(40, 128)
        btn1.clicked.connect(partial(self._previous_item, grid.itemAt(0).layout()))
        grid.addWidget(btn1, 0, 0)
        btn2 = QPushButton('>')
        btn2.setObjectName('next_item')
        btn2.setMaximumSize(40, 128)
        btn2.clicked.connect(partial(self._next_item, grid.itemAt(0).layout()))
        grid.addWidget(btn2, 0, 2)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 98)
        grid.setColumnStretch(2, 1)
        return grid

    def _create_group(self, i, item=None):
        layout = QGridLayout()

        # Image
        image_path = explorer.get_image(item['id'], constants.product_image_filepath())
        pixmap = QPixmap(image_path)
        pixmap2 = pixmap.scaledToHeight(128)
        image = QLabel()
        image.setPixmap(pixmap2)
        image.setAlignment(Qt.AlignCenter)
        image.setWordWrap(True)

        # Name
        name = QLabel(item['name'])
        name.setStyleSheet('font-weight: bold; font-size: 18px;')
        name.setWordWrap(True)

        # Price
        price = QLabel(str(item['price']))
        price.setStyleSheet('font-size: 14px; font-weight: bold;')
        price.setAlignment(Qt.AlignCenter)
        price.setWordWrap(True)

        # Description
        text = 'In publishing and graphic design, Lorem ipsum is a placeholder text commonly' \
               ' used to demonstrate the visual form of a document or a typeface without relying' \
               ' on meaningful content. Lorem ipsum may be used as a placeholder before final copy is available.'
        desc = QLabel(text)
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
        label.setStyleSheet('QLabel {border: 1px solid green; background-color: white;} QClickLabel::hover {background-color: #cfffd3;}')
        label.clicked.connect(partial(self.change_to_product, item['id'], item['supplier_id'], image_path, item['name'], item['price'], item['description']))
        return label


app = QApplication(sys.argv)
win = Window()
win.resize(700, 700)
win.show()
sys.exit(app.exec_())

from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QWidget, QLineEdit
from core.users import Customer, Supplier, Operator


class CustomerLoginView(QWidget):
    def __init__(self, parent_widget, parent=None):
        super().__init__(parent)
        self.parent_widget = parent_widget
        self.setLayout(self.setUI())
        self.setStyleSheet('border: 1px solid red; background-color: white;')

    def setUI(self):
        login_button = QPushButton("Login")
        layout = QVBoxLayout()

        phone_label = QLabel("PHONE")
        password_label = QLabel("PASSWORD")

        self.phone_textbox = QLineEdit()
        self.phone_textbox.setPlaceholderText('Enter your phone number')
        self.password_textbox = QLineEdit()
        self.password_textbox.setPlaceholderText('Enter your password')

        login_button.clicked.connect(self._get_user)

        layout.addWidget(phone_label)
        layout.addWidget(self.phone_textbox)
        layout.addWidget(password_label)
        layout.addWidget(self.password_textbox)
        layout.addWidget(login_button)

        return layout

    def _get_user(self):
        user = Customer.get_object(self.phone_textbox.text())
        if user['password'] == self.password_textbox.text():
            user['type'] = 'customer'
            user = self.parent_widget.window().build_user(user)
            parent_window = self.parent_widget.window()
            parent_window.set_user(user, True)
            parent_window._usertype = 'customer'
            parent_window.change_to_main()
            parent_window.enable_logout()
        else:
            print('false')


class SupplierLoginView(QWidget):
    def __init__(self, parent_widget, parent=None):
        super().__init__(parent)
        self.parent_widget = parent_widget
        self.setLayout(self.setUI())
        self.setStyleSheet('border: 1px solid red; background-color: white;')

    def setUI(self):
        login_button = QPushButton("Login")
        layout = QVBoxLayout()

        phone_label = QLabel('Phone')
        password_label = QLabel('Password')

        self.phone_textbox = QLineEdit()
        self.phone_textbox.setPlaceholderText('Enter your phone number')
        self.password_textbox = QLineEdit()
        self.password_textbox.setPlaceholderText('Enter your password')

        login_button.clicked.connect(self._get_user)

        layout.addWidget(phone_label)
        layout.addWidget(self.phone_textbox)
        layout.addWidget(password_label)
        layout.addWidget(self.password_textbox)
        layout.addWidget(login_button)

        return layout

    def _get_user(self):
        user = Supplier.get_object(self.phone_textbox.text())
        if user['password'] == self.password_textbox.text():
            user['type'] = 'supplier'
            user = self.parent_widget.window().build_user(user)
            parent_window = self.parent_widget.window()
            parent_window.set_user(user, True)
            parent_window._usertype = 'supplier'
            parent_window.change_to_main()
            parent_window.enable_logout()
        else:
            print('false')


class OperatorLoginView(QWidget):
    def __init__(self, parent_widget, parent=None):
        super().__init__(parent)
        self.parent_widget = parent_widget
        self.setLayout(self.setUI())
        self.setStyleSheet('border: 1px solid red; background-color: white;')

    def setUI(self):
        login_button = QPushButton("Login")
        layout = QVBoxLayout()

        phone_label = QLabel('Phone')
        password_label = QLabel('Password')

        self.phone_textbox = QLineEdit()
        self.phone_textbox.setPlaceholderText('Enter your phone number')
        self.password_textbox = QLineEdit()
        self.password_textbox.setPlaceholderText('Enter your password')

        login_button.clicked.connect(self._get_user)

        layout.addWidget(phone_label)
        layout.addWidget(self.phone_textbox)
        layout.addWidget(password_label)
        layout.addWidget(self.password_textbox)
        layout.addWidget(login_button)

        return layout

    def _get_user(self):
        user = Operator.get_object(self.phone_textbox.text())
        if user['password'] == self.password_textbox.text():
            user['type'] = 'operator'
            user = self.parent_widget.window().build_user(user)
            parent_window = self.parent_widget.window()
            parent_window.set_user(user, True)
            parent_window._usertype = 'operator'
            parent_window.change_to_main()
            parent_window.enable_logout()
        else:
            print('false')

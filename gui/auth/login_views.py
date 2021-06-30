from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QWidget, QLineEdit
from core.users import Customer, Supplier, Operator


class CustomerLoginView(QWidget):
    def __init__(self, login_method, parent=None):
        super().__init__(parent)
        self.login_method = login_method
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
            self.login_method(user, user['type'])

        else:
            print('false')


class SupplierLoginView(QWidget):
    def __init__(self, login_method, parent=None):
        super().__init__(parent)
        self.login_method = login_method
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
            self.login_method(user, user['type'])
        else:
            print('false')


class OperatorLoginView(QWidget):
    def __init__(self, login_method, parent=None):
        super().__init__(parent)
        self.login_method = login_method
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
            self.login_method(user, user['type'])
        else:
            print('false')

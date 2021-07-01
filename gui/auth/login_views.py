from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QWidget, QLineEdit, QMessageBox
from core.users import Customer, Supplier, Operator


class CustomerLoginView(QWidget):
    def __init__(self, login_method, parent=None):
        super().__init__(parent)
        self.login_method = login_method
        self.setLayout(self.setUI())
        self.setStyleSheet('border: 1px solid green; background-color: white;')

    def setUI(self):
        login_button = QPushButton("Login")
        login_button.setMinimumHeight(96)
        login_button.setStyleSheet('QPushButton::hover {background-color: limegreen;} QPushButton {background-color: gray; font-size: 28px;}')
        layout = QVBoxLayout()

        phone_label = QLabel("PHONE")
        password_label = QLabel("PASSWORD")

        self.phone_textbox = QLineEdit()
        self.phone_textbox.setMinimumHeight(64)
        self.phone_textbox.setPlaceholderText('Enter your phone number')
        self.password_textbox = QLineEdit()
        self.password_textbox.setMinimumHeight(64)
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
            QMessageBox.about(self, 'Error', 'Please enter valid credentials')


class SupplierLoginView(QWidget):
    def __init__(self, login_method, parent=None):
        super().__init__(parent)
        self.login_method = login_method
        self.setLayout(self.setUI())
        self.setStyleSheet('border: 1px solid green; background-color: white;')

    def setUI(self):
        login_button = QPushButton("Login")
        login_button.setMinimumHeight(96)
        login_button.setStyleSheet('QPushButton::hover {background-color: limegreen;} QPushButton {background-color: gray; font-size: 28px;}')
        layout = QVBoxLayout()

        phone_label = QLabel('Phone')
        password_label = QLabel('Password')

        self.phone_textbox = QLineEdit()
        self.phone_textbox.setMinimumHeight(64)
        self.phone_textbox.setPlaceholderText('Enter your phone number')
        self.password_textbox = QLineEdit()
        self.password_textbox.setMinimumHeight(64)
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
            QMessageBox.about(self, 'Error', 'Please enter valid credentials')


class OperatorLoginView(QWidget):
    def __init__(self, login_method, parent=None):
        super().__init__(parent)
        self.login_method = login_method
        self.setLayout(self.setUI())
        self.setStyleSheet('border: 1px solid green; background-color: white;')

    def setUI(self):
        login_button = QPushButton("Login")
        login_button.setMinimumHeight(96)
        login_button.setStyleSheet('QPushButton::hover {background-color: limegreen;} QPushButton {background-color: gray; font-size: 28px;}')
        layout = QVBoxLayout()

        phone_label = QLabel('Phone')
        password_label = QLabel('Password')

        self.phone_textbox = QLineEdit()
        self.phone_textbox.setMinimumHeight(64)
        self.phone_textbox.setPlaceholderText('Enter your phone number')
        self.password_textbox = QLineEdit()
        self.password_textbox.setMinimumHeight(64)
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
            QMessageBox.about(self, 'Error', 'Please enter valid credentials')

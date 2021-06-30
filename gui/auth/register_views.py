from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QWidget, QLineEdit, QMessageBox
from core.users import Customer, Supplier, Operator
from core import explorer, constants


class CustomerRegisterView(QWidget):
    def __init__(self, register_method, parent=None):
        super().__init__(parent)
        self.register_method = register_method
        self.setLayout(self.setUI())
        self.setStyleSheet('border: 1px solid red; background-color: white;')

    def setUI(self):
        register_button = QPushButton('REGISTER')
        layout = QVBoxLayout()

        phone_label = QLabel('Phone')
        email_label = QLabel('E-mail')
        password_label = QLabel('Password')
        confirm_password_label = QLabel('Confirm Password')

        self.phone_textbox = QLineEdit()
        self.phone_textbox.setPlaceholderText('Enter your phone number')
        self.email_textbox = QLineEdit()
        self.email_textbox.setPlaceholderText('Enter your E-mail address (optional)')
        self.password_textbox = QLineEdit()
        self.password_textbox.setPlaceholderText('Enter your password')
        self.confirm_password_textbox = QLineEdit()
        self.confirm_password_textbox.setPlaceholderText('Re-Enter your password')

        register_button.clicked.connect(self._create_user)

        layout.addWidget(phone_label)
        layout.addWidget(self.phone_textbox)
        layout.addWidget(email_label)
        layout.addWidget(self.email_textbox)
        layout.addWidget(password_label)
        layout.addWidget(self.password_textbox)
        layout.addWidget(confirm_password_label)
        layout.addWidget(self.confirm_password_textbox)
        layout.addWidget(register_button)

        return layout

    def _create_user(self):
        if self.password_textbox.text() == self.confirm_password_textbox.text():
            for u in explorer.get_all(constants.customer_filepath()):
                if int(self.phone_textbox.text()) == u['phone'] or self.email_textbox.text() == u['email']:
                    QMessageBox.about(self, 'Error', 'duplicate phone number or email')
                    return
            user = Customer(self.phone_textbox.text(), self.email_textbox.text(), self.password_textbox.text())
            self.register_method(user, 'customer')
        else:
            QMessageBox.about(self, 'Error', 'Passwords do not match!')


class SupplierRegisterView(QWidget):
    def __init__(self, register_method, parent=None):
        super().__init__(parent)
        self.register_method = register_method
        self.setLayout(self.setUI())
        self.setStyleSheet('border: 1px solid red; background-color: white;')

    def setUI(self):
        register_button = QPushButton("REGISTER")
        layout = QVBoxLayout()

        firstname_label = QLabel('First Name')
        lastname_label = QLabel('Last Name')
        address_label = QLabel('Address')
        phone_label = QLabel('Phone')
        email_label = QLabel('E-mail')
        password_label = QLabel('Password')
        confirm_password_label = QLabel('Confirm Password')

        self.firstname_textbox = QLineEdit()
        self.firstname_textbox.setPlaceholderText('Enter your first name')
        self.lastname_textbox = QLineEdit()
        self.lastname_textbox.setPlaceholderText('Enter your last name')
        self.address_textbox = QLineEdit()
        self.address_textbox.setPlaceholderText('Enter your address')
        self.phone_textbox = QLineEdit()
        self.phone_textbox.setPlaceholderText('Enter your phone number')
        self.email_textbox = QLineEdit()
        self.email_textbox.setPlaceholderText('Enter your E-mail address (optional)')
        self.password_textbox = QLineEdit()
        self.password_textbox.setPlaceholderText('Enter your password')
        self.confirm_password_textbox = QLineEdit()
        self.confirm_password_textbox.setPlaceholderText('Re-Enter your password')

        register_button.clicked.connect(self._create_user)

        layout.addWidget(phone_label)
        layout.addWidget(self.phone_textbox)
        layout.addWidget(firstname_label)
        layout.addWidget(self.firstname_textbox)
        layout.addWidget(lastname_label)
        layout.addWidget(self.lastname_textbox)
        layout.addWidget(address_label)
        layout.addWidget(self.address_textbox)
        layout.addWidget(email_label)
        layout.addWidget(self.email_textbox)
        layout.addWidget(password_label)
        layout.addWidget(self.password_textbox)
        layout.addWidget(confirm_password_label)
        layout.addWidget(self.confirm_password_textbox)
        layout.addWidget(register_button)

        return layout

    def _create_user(self):
        if self.password_textbox.text() == self.confirm_password_textbox.text():
            for u in explorer.get_all(constants.supplier_logs_filepath()):
                if int(self.phone_textbox.text()) == u['phone'] or self.email_textbox.text() == u['email']:
                    QMessageBox.about(self, 'Error', 'duplicate phone number or email')
                    return
            user = Supplier(self.firstname_textbox.text(), self.lastname_textbox.text(), self.address_textbox.text(),
                            self.phone_textbox.text(), self.email_textbox.text(), self.password_textbox.text())
            self.register_method(user, 'supplier')
        else:
            QMessageBox.about(self, 'Error', 'Passwords do not match!')


class OperatorRegisterView(QWidget):
    def __init__(self, register_method, parent=None):
        super().__init__(parent)
        self.register_method = register_method
        self.setLayout(self.setUI())
        self.setStyleSheet('border: 1px solid red; background-color: white;')

    def setUI(self):
        register_button = QPushButton("REGISTER")
        layout = QVBoxLayout()

        firstname_label = QLabel('First Name')
        lastname_label = QLabel('Last Name')
        phone_label = QLabel('Phone')
        email_label = QLabel('E-mail')
        password_label = QLabel('Password')
        confirm_password_label = QLabel('Confirm Password')

        self.firstname_textbox = QLineEdit()
        self.firstname_textbox.setPlaceholderText('Enter your first name')
        self.lastname_textbox = QLineEdit()
        self.lastname_textbox.setPlaceholderText('Enter your last name')
        self.phone_textbox = QLineEdit()
        self.phone_textbox.setPlaceholderText('Enter your phone number')
        self.email_textbox = QLineEdit()
        self.email_textbox.setPlaceholderText('Enter your E-mail address (optional)')
        self.password_textbox = QLineEdit()
        self.password_textbox.setPlaceholderText('Enter your password')
        self.confirm_password_textbox = QLineEdit()
        self.confirm_password_textbox.setPlaceholderText('Re-Enter your password')

        register_button.clicked.connect(self._create_user)

        layout.addWidget(phone_label)
        layout.addWidget(self.phone_textbox)
        layout.addWidget(firstname_label)
        layout.addWidget(self.firstname_textbox)
        layout.addWidget(lastname_label)
        layout.addWidget(self.lastname_textbox)
        layout.addWidget(email_label)
        layout.addWidget(self.email_textbox)
        layout.addWidget(password_label)
        layout.addWidget(self.password_textbox)
        layout.addWidget(confirm_password_label)
        layout.addWidget(self.confirm_password_textbox)
        layout.addWidget(register_button)

        return layout

    def _create_user(self):
        if self.password_textbox.text() == self.confirm_password_textbox.text():
            for u in explorer.get_all(constants.operator_filepath()):
                if int(self.phone_textbox.text()) == u['phone'] or self.email_textbox.text() == u['email']:
                    QMessageBox.about(self, 'Error', 'duplicate phone number or email')
                    return
            user = Operator(self.firstname_textbox.text(), self.lastname_textbox.text(),
                            self.phone_textbox.text(), self.email_textbox.text(), self.password_textbox.text())
            self.register_method(user, 'operator')
        else:
            QMessageBox.about(self, 'Error', 'Passwords do not match!')

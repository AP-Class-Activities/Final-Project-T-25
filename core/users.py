# This file holds classes for all the online shop users
# including customers, suppliers and operators
# THIS FILE IS SUBJECT TO CHANGE

import re
from core import constants, explorer


class User:
    """Base class for all users"""
    def __init__(self, phone, email, password):
        self.phone = phone
        self.email = email
        self.password = password
        self.id = self.give_id()

    def set_current_user(self):
        pass

    @staticmethod
    def give_id():
        """should be implemented with files"""
        return explorer.get_next_id(constants.customer_filepath())

    def check_password(self, old_password):
        """checks password matching"""
        if self.__password == old_password:
            return True

    def change_password(self, new_password):
        self.__password = new_password

    @property
    def firstname(self):
        return self.__firstname

    @firstname.setter
    def firstname(self, value):
        if not isinstance(value, str):
            raise ValueError("the name should be string!!")
        elif len(value) > 30:
            raise ValueError("the firstname should be less than 30 character!")
        self.__firstname = value

    @property
    def lastname(self):
        return self.__lastname

    @lastname.setter
    def lastname(self, value):
        if not isinstance(value, str):
            raise ValueError("the lastname should be string!!")
        elif len(value) > 50:
            raise ValueError("the lastname should be less than 50 character!")

        self.__lastname = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        pattern = r'[\w\.-]+@[\w\.-]+(\.[\w]+)+'
        if not isinstance(value, str) or not re.search(pattern, value):
            raise ValueError("attribute *email* must be instance of <str>")
        self.__email = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        pattern = '[A-Za-z0-9@#$%^&+=]{8,}'
        if not isinstance(value, str) or not re.fullmatch(pattern, value):
            raise ValueError("attribute *password* must be instance of <str>")
        self.__password = value

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        if not isinstance(value, int):
            try:
                value = int(value)
            except ValueError:
                raise ValueError('incorrect value for attribute phone')
        elif len(str(value)) != 10:
            raise ValueError('attribute *phone* must be exactly 11 numbers')
        self.__phone = value

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError('attribute *id* must be an instance of <int>')
        self.__id = value


class Customer(User):
    """Inherits from User"""
    def __init__(self, phone, email, password, save_to_database=True):
        super().__init__(phone, email, password)
        self.wallet = 0
        self.is_active = True
        if save_to_database:
            self._save()

    @staticmethod
    def get_object(phone_number):
        if isinstance(phone_number, str):
            try:
                phone_number = int(phone_number)
            except ValueError:
                raise ValueError('cannot convert phone_number to type int')
        return explorer.search_phone(phone_number, constants.customer_filepath())

    def update(self):
        explorer.overwrite(constants.customer_filepath(), self)

    def set_current_user(self):
        explorer.save_session(self, constants.session_filepath(), 'customer')

    def _save(self):
        explorer.save(self, constants.customer_filepath())

    def charge_wallet(self, amount):
        self.__wallet += amount

    def add_to_favorites(self, name):
        """should be implemented with files"""
        pass

    def remove_from_favorites(self, name):
        """should be implemented with files"""
        pass

    def get_fav_list(self):
        """should be implemented with files"""
        pass

    @property
    def wallet(self):
        return self.__wallet

    @wallet.setter
    def wallet(self, value):
        if not isinstance(value, int):
            raise ValueError('wallet should be integer')
        self.__wallet = value

    @property
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_active should be bool!!")
        self.__is_active = value

    def __iter__(self):
        yield from self.__dict__.items()


class Supplier(User):

    def __init__(self, firstname, lastname, address, phone, email, password, save_to_database=True):
        super().__init__(phone, email, password)
        self.firstname = firstname
        self.lastname = lastname
        self.point = 50
        self.wallet = 0
        self.is_active = False
        self.is_approved = False
        self.address = address
        if save_to_database:
            self._save()

    @staticmethod
    def get_object(phone_number):
        if isinstance(phone_number, str):
            try:
                phone_number = int(phone_number)
            except ValueError:
                raise ValueError('cannot convert phone_number to type int')
        return explorer.search_phone(phone_number, constants.supplier_filepath())

    def update(self):
        explorer.overwrite(constants.supplier_filepath(), self)

    def set_current_user(self):
        explorer.save_session(self, constants.session_filepath(), 'supplier')

    def _save(self):
        explorer.save(self, constants.supplier_filepath())

    def calculate_point(self):
        pass

    @property
    def point(self):
        return self.__point

    @point.setter
    def point(self, value):
        if not isinstance(value, int):
            raise ValueError("the point should be integer!!")
        self.__point = value

    @property
    def wallet(self):
        return self.__wallet

    @wallet.setter
    def wallet(self, value):
        if not isinstance(value, int):
            raise ValueError("wallet should be integer")
        self.__wallet = value

    @property
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_active should be bool!!")
        self.__is_active = value

    @property
    def is_approved(self):
        return self.__is_approved

    @is_approved.setter
    def is_approved(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_approved should be bool!!")
        self.__is_approved = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        if not isinstance(value, str):
            raise ValueError("the address should be string!!")
        self.__address = value

    def __iter__(self):
        yield from self.__dict__.items()


class Operator(User):
    def __init__(self, firstname, lastname, phone, email, password, save_to_database=True):
        super().__init__(phone, email, password)
        self.firstname = firstname
        self.lastname = lastname
        self.is_active = True
        if save_to_database:
            self._save()

    @staticmethod
    def get_object(phone_number):
        if isinstance(phone_number, str):
            try:
                phone_number = int(phone_number)
            except ValueError:
                raise ValueError('cannot convert phone_number to type int')
        return explorer.search_phone(phone_number, constants.operator_filepath())

    def update(self):
        explorer.overwrite(constants.operator_filepath(), self)

    def set_current_user(self):
        explorer.save_session(self, constants.session_filepath(), 'operator')

    def _save(self):
        explorer.save(self, constants.operator_filepath())

    @property
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_active should be bool!!")
        self.__is_active = value

    def __iter__(self):
        yield from self.__dict__.items()

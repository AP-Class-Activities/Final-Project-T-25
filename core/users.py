# This file holds classes for all the online shop users
# including customers, suppliers and operators
# THIS FILE IS SUBJECT TO CHANGE

import re


class User:
    """Base class for all users"""
    def __init__(self, firstname, lastname, email, password, phone):
        self.__firstname = firstname
        self.__lastname = lastname
        self.__email = email
        self.__password = password
        self.__phone = phone
        self.__id = self.give_id()

    def give_id(self):
        """should be implemented with files"""
        pass

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
        pattern = '^(\w\-\_\.)+[@](\w|\-\_\.)+[.]\w{2,3}$'
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
            raise ValueError("attribute *phone* must be instance of <int>")
        elif len(value) != 11:
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
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.__wallet = 0
        self.__is_active = True
        self.__cart = []

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

    @property
    def cart(self):
        return self.__cart

    @cart.setter
    def cart(self, value):
        if not isinstance(value, str):
            raise ValueError("attribute *value* must be instance of <str>")
        self.__cart.append(value)


class Supplier(User):

    def __init__(self, address, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.__point = 50
        self.__wallet = 0
        self.__is_active = False
        self.__address = address

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
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        if not isinstance(value, str):
            raise ValueError("the address should be string!!")
        self.__address = value


class Operator(User):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.__is_active = True

    @property
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_active should be bool!!")
        self.__is_active = value

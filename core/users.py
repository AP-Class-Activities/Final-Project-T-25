class User:

    def __init__(self, firstname, lastname):
        self.__firstname = firstname
        self.__lastname = lastname

    def give_id(self):
        pass

    @property
    def firstname(self):
        return self.__firstname

    @firstname.setter
    def firstname(self, value):
        if not isinstance(value, str):
            raise ValueError("the name should be string!!")
        self.__firstname = value

    @property
    def lastname(self):
        return self.__lastname

    @lastname.setter
    def lastname(self, value):
        if not isinstance(value, str):
            raise ValueError("the lastname should be string!!")
        self.__lastname = value


class Customer(User):

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.__wallet = 0
        self.__is_active = True

    def charge_wallet(self, amount):
        pass

    def add_to_favorites(self, name):
        pass

    def remove_from_favorites(self, name):
        pass

    def get_fav_list(self):
        pass

    def get_buy_list(self):
        pass

    @property
    def wallet(self):
        return self.__wallet

    @wallet.setter
    def wallet(self, value):
        if not isinstance(value,int):
            raise ValueError("wallet should be integer")
        self.__wallet = value


    @property
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self, value):
        if not isinstance(value,bool):
            raise ValueError("is_active should be bool!!")
        self.__is_active = value


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
        if not isinstance(value,int):
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
        if not isinstance(value,bool):
            raise ValueError("is_active should be bool!!")
        self.__is_active = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        if not isinstance(value,str):
            raise ValueError("the address should be string!!")
        self.__address= value


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
import datetime
from core import explorer, constants
import os


log = {"items": [[35, 235, 25425]], "is_delivered": False}


class SupplierLog:
    def __init__(self, supplier_id, items, save_to_database=False):
        self.__items = []
        self.items = items
        self.supplier_id = supplier_id
        self.time = datetime.datetime.now().strftime('%Y-%m-%d')
        self.is_delivered = False
        self.id = self.give_id()
        if save_to_database:
            self.save()

    def give_id(self):
        return explorer.get_next_id(os.path.join(constants.supplier_logs_filepath(), str(self.supplier_id)))

    def save(self):
        path = os.path.join(constants.supplier_logs_filepath(), str(self.supplier_id))
        explorer.save(self, path)

    @property
    def supplier_id(self):
        return self.__supplier_id

    @supplier_id.setter
    def supplier_id(self, value):
        if not isinstance(value, int):
            raise ValueError('comment supplier_id must be instance of <int>')
        self.__supplier_id = value

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, value):
        for i in value:
            self.__items.append(i)

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, value):
        self.__time = value

    @property
    def is_delivered(self):
        return self.__is_delivered

    @is_delivered.setter
    def is_delivered(self, value):
        self.__is_delivered = value

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    def __iter__(self):
        for k, v in self.__dict__.items():
            if k == '_SupplierLog__supplier_id':
                continue
            elif k == '_SupplierLog__items':
                v = [[int(num) for num in sub] for sub in self.__items]
            yield k, v

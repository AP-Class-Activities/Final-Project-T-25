import datetime
from core import explorer, constants
import os


class History:
    def __init__(self, customer_id, items, save_to_database=False):
        self.__items = {}
        self.items = items
        self.customer_id = customer_id
        self.time = datetime.datetime.now().strftime('%Y-%m-%d')
        if save_to_database:
            self.save()

    def save(self):
        path = os.path.join(constants.history_filepath() + '/' + str(self.customer_id))
        explorer.save(self, path)

    @property
    def customer_id(self):
        return self.__customer_id

    @customer_id.setter
    def customer_id(self, value):
        if not isinstance(value, int):
            raise ValueError('comment customer_id must be instance of <int>')
        self.__customer_id = value

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, value):
        for k, v in value.items():
            self.__items[k] = v

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, value):
        self.__time = value

    def __iter__(self):
        for k, v in self.__dict__.items():
            if k == '_History__customer_id':
                continue
            yield k, v

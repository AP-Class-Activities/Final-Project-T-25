from core import explorer, constants


class Product:

    def __init__(self, category, name, weight, desc, price, count, supplier_id, save_to_database=True):
        self.category = category
        self.name = name
        self.weight = weight
        self.description = desc
        self.price = price
        self.count = count
        self.supplier_id = supplier_id
        self.rating = '0-0-0-0-0'  # this attr holds the number of votes (from 1 to 5 points) in descending order
        self.id = self.give_id()
        self.is_available = True
        self.is_approved = False
        if save_to_database:
            self._save()

    def calc_point(self):
        """calculates total point of product using attribute *rating* by turning
         the string into list of integers and applying the weighted average"""
        votes = list(map(int, self.__rating.split('-')))
        return (5 * votes[4] + 4 * votes[3] + 3 * votes[2] + 2 * votes[1] + 1 * votes[0]) / sum(votes)

    def check_available(self):
        if self.count == 0:
            self.__is_available = False

    @staticmethod
    def give_id():
        return explorer.get_next_id(constants.product_data_filepath())

    def reduce_count(self, quantity):
        """reduces count of product when it is bought"""
        self.__count -= quantity

    def _save(self):
        explorer.save(self, constants.product_data_filepath())

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise ValueError('attribute *category* must be an instance of <str>')
        self.__category = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError('attribute *name* must be an instance of <str>')
        self.__name = value

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        if not isinstance(value, int):
            raise ValueError('attribute *weight* must be an instance of <int>')
        elif value < 0:
            raise ValueError('attribute *weight* must be positive')
        self.__weight = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise ValueError('attribute *description* must be an instance of <str>')
        elif len(value) > 125:
            raise ValueError('description too long')
        self.__description = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if not isinstance(value, int):
            raise ValueError('attribute *price* must be an instance of <int>')
        elif value < 0:
            raise ValueError('attribute *price* must be positive')
        self.__price = value

    @property
    def count(self):
        return self.__count

    @count.setter
    def count(self, value):
        if not isinstance(value, int):
            raise ValueError('attribute *price* must be an instance of <int>')
        elif value < 0:
            raise ValueError('attribute *count* cannot be negative')
        self.__count = value

    @property
    def supplier_id(self):
        return self.__supplier_id

    @supplier_id.setter
    def supplier_id(self, value):
        if not isinstance(value, int):
            raise ValueError('attribute *supplier_id* must be an instance of <int>')
        self.__supplier_id = value

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, str):
            raise ValueError('attribute *rating* must be an instance of <str>')
        try:
            for vote in list(map(int, self.__rating.split('-'))):
                if vote < 0:
                    raise ValueError('votes of attribute *rating* must be positive')
        except AttributeError:
            pass
        self.__rating = value

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError('attribute *id* must be an instance of <int>')
        self.__id = value

    @property
    def is_available(self):
        return self.__is_available

    @is_available.setter
    def is_available(self, value):
        if not isinstance(value, bool):
            raise ValueError('attribute *is_available* must be an instance of <bool>')
        self.__is_available = value

    @property
    def is_approved(self):
        return self.__is_approved

    @is_approved.setter
    def is_approved(self, value):
        if not isinstance(value, bool):
            raise ValueError('attribute *is_approved* must be an instance of <bool>')
        self.__is_approved = value

    def __iter__(self):
        temp = self.__dict__
        temp.update({'rating': '0-0-0-0-0'})
        yield from temp.items()

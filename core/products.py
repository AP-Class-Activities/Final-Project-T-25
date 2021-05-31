class Product:

    def __init__(self, name, point, weight, desc, price, count):
        self.name = name
        self.weight = weight
        self.description = desc
        self.price = price
        self.point = point
        self.count = count
        self.id = self.give_id()
        self.is_available = True
        self.is_approved = False

    def calculate_point(self):
        pass

    def give_id(self):
        return 'id'

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def point(self):
        return self.__point

    @point.setter
    def point(self, value):
        self.__point = value

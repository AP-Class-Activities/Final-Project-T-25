from core import explorer, constants


class Cart:
    def __init__(self, customer_id, items=None, save_to_database=False):
        if items is None:
            items = {}
        self.id = customer_id
        self.items = items
        if save_to_database:
            self.save()

    def add_item(self, product_id, quantity, price, supplier_id):
        if product_id in self.items:
            self.items[product_id][0] += quantity
        else:
            self.items[product_id] = [quantity, price, supplier_id]
        explorer.overwrite(constants.cart_filepath(), self)

    def flush_cart(self):
        self.items = {}
        self.update_cart()

    def update_cart(self):
        explorer.overwrite(constants.cart_filepath(), self)

    def save(self):
        explorer.save_cart(constants.cart_filepath(), self)

    def total(self):
        total_price = 0
        for k, v in self.__items.items():
            total_price += int(v[0]) * int(v[1])
        return total_price

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError('cart id must be an instance of <int>')
        self.__id = value

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, value):
        if not isinstance(value, dict):
            raise ValueError('cart items must be an instance of <dict>')
        self.__items = value

    def __iter__(self):
        yield from self.__dict__.items()

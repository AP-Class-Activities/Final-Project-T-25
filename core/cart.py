from core import explorer, constants


class Cart:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.items = {}
        self.save()

    def add_item(self, product_id, quantity, price, supplier_id):
        self.items[product_id] = [quantity, price, supplier_id]

    def flush_cart(self):
        self.items = {}
        self.update_cart()

    def update_cart(self):
        explorer.overwrite(constants.cart_filepath(), self)

    def save(self):
        explorer.save_cart(constants.cart_filepath(), self)

    @property
    def customer_id(self):
        return self.__customer_id

    @customer_id.setter
    def customer_id(self, value):
        if not isinstance(value, int):
            raise ValueError('cart customer_id must be an instance of <int>')
        self.__customer_id = value

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

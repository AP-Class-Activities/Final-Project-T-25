from core import explorer
from core import constants


class Comment:
    def __init__(self, text, rating, user_id, product_id, save_to_database=False):
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.product_id = product_id
        if save_to_database:
            self.save()

    def save(self):
        explorer.save_comment(constants.product_comments_filepath(), self)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise ValueError('comment text must be instance of <str>')
        elif len(value) >= 120:
            raise ValueError('length of comment text must be less than or equal to 120 characters')
        self.__text = value

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int):
            raise ValueError('comment rating must be instance of <int>')
        elif not 1 <= value <= 5:
            raise ValueError('comment rating must be a number between(including) 1 and 5')
        self.__rating = value

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        if not isinstance(value, int):
            raise ValueError('comment user_id must be instance of <int>')
        self.__user_id = value

    @property
    def product_id(self):
        return self.__product_id

    @product_id.setter
    def product_id(self, value):
        if not isinstance(value, int):
            raise ValueError('comment product_id must be instance of <int>')
        self.__product_id = value

    def __iter__(self):
        for k, v in self.__dict__.items():
            if k == '_Comment__product_id':
                continue
            yield k, v

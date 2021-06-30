import os


FILE_LIMIT = 5

CATEGORIES = ['Electronics', 'Edibles', 'Clothes', 'Skin Care', 'Kitchen', 'Books']

FILE_STORAGE_PATH = 'database/'

PRODUCTS_FILEPATH = FILE_STORAGE_PATH + 'products/'
USERS_FILEPATH = FILE_STORAGE_PATH + 'users/'
HISTORY_FILEPATH = FILE_STORAGE_PATH + 'history/'
SUPPLIER_LOGS_FILEPATH = FILE_STORAGE_PATH + 'supplier_logs/'
CART_FILEPATH = FILE_STORAGE_PATH + 'cart/'
SESSION_FILEPATH = FILE_STORAGE_PATH + 'session/'

PRODUCT_DATA_FILEPATH = PRODUCTS_FILEPATH + 'data/'
PRODUCT_IMAGE_FILEPATH = PRODUCTS_FILEPATH + 'images/'
PRODUCT_COMMENTS_FILEPATH = PRODUCTS_FILEPATH + 'comments/'

CUSTOMERS_FILEPATH = USERS_FILEPATH + 'customers/'
SUPPLIERS_FILEPATH = USERS_FILEPATH + 'suppliers/'
OPERATORS_FILEPATH = USERS_FILEPATH + 'operators/'


def get_path(relative_path):
    if 'core' in os.getcwd() or 'gui' in os.getcwd():
        return os.path.abspath('../' + relative_path)
    return os.path.abspath(relative_path)


def product_data_filepath():
    return get_path(PRODUCT_DATA_FILEPATH)


def product_image_filepath():
    return get_path(PRODUCT_IMAGE_FILEPATH)


def product_comments_filepath():
    return get_path(PRODUCT_COMMENTS_FILEPATH)


def customer_filepath():
    return get_path(CUSTOMERS_FILEPATH)


def supplier_filepath():
    return get_path(SUPPLIERS_FILEPATH)


def operator_filepath():
    return get_path(OPERATORS_FILEPATH)


def history_filepath():
    return get_path(HISTORY_FILEPATH)


def supplier_logs_filepath():
    return get_path(SUPPLIER_LOGS_FILEPATH)


def cart_filepath():
    return get_path(CART_FILEPATH)


def session_filepath():
    return get_path(SESSION_FILEPATH)

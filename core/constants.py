import os


FILE_LIMIT = 5


FILE_STORAGE_PATH = 'database/'

PRODUCT_FILEPATH = FILE_STORAGE_PATH + 'products'
CUSTOMERS_FILEPATH = FILE_STORAGE_PATH + 'customers'
SUPPLIERS_FILEPATH = FILE_STORAGE_PATH + 'suppliers'
OPERATORS_FILEPATH = FILE_STORAGE_PATH + 'operators'


def get_path(relative_path):
    if 'core' in os.getcwd():
        return os.path.abspath('../' + relative_path)
    return os.path.abspath(relative_path)


def product_filepath():
    return get_path(PRODUCT_FILEPATH)


def customer_filepath():
    return get_path(CUSTOMERS_FILEPATH)


def supplier_filepath():
    return get_path(SUPPLIERS_FILEPATH)


def operator_filepath():
    return get_path(OPERATORS_FILEPATH)

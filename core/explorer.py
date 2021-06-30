import json
import os
from core import constants
from pathlib import Path
import shutil


def make_directory(path_to_directory):
    p = Path(path_to_directory)
    p.mkdir(exist_ok=True, parents=True)


def beautify_key(string):
    try:
        index = string.index('__')
        if index <= 0:
            return string
    except ValueError:
        return string
    return string[index + 2:]


def beautify_all(obj):
    return {beautify_key(k): v for k, v in dict(obj).items()}  # DON'T call __dict__ on objects


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        return beautify_all(obj)


def save_session(obj, dirname, user_type):
    obj = beautify_all(obj)
    obj['type'] = user_type
    if not os.path.isdir(dirname):
        make_directory(dirname)
    with open(dirname + '\\' + 'session.json', 'w') as file:
        json.dump(obj, file)


def get_user():
    path = constants.session_filepath() + '\\' + 'session.json'
    try:
        if os.stat(path).st_size == 0:
            return None
        with open(path, 'r') as file:
            user = json.loads(file.readline())
        if not user:
            return None
        return user
    except FileNotFoundError:
        return None


def flush_session():
    try:
        open(constants.session_filepath() + '\\' + 'session.json', 'w').close()
    except FileNotFoundError:
        pass


def save_cart(dirname, obj):
    if not os.path.isdir(dirname):
        make_directory(dirname)
    filename = get_filename(dirname)
    with open(os.path.join(dirname + '/' + filename), 'a+') as file:
        json.dump(obj, file, cls=CustomEncoder)
        file.write('\n')


def save_history(dirname, obj):
    dirname += f'/{obj.id}'
    if not os.path.isdir(dirname):
        make_directory(dirname)
    if not os.listdir(dirname):
        json_file = '1.json'
    else:
        json_file = sorted(os.listdir(dirname))[-1]
        if count_objects(json_file, dirname) >= constants.FILE_LIMIT:
            json_file = str(int(json_file[0]) + 1) + '.json'
    with open(os.path.join(dirname + '/' + json_file), 'a+') as file:
        json.dump(obj, file, cls=CustomEncoder)
        file.write('\n')


def save_comment(dirname, obj):
    dirname += f'/{obj.product_id}'
    if not os.path.isdir(dirname):
        make_directory(dirname)
    if not os.listdir(dirname):
        json_file = '1.json'
    else:
        json_file = sorted(os.listdir(dirname))[-1]
        if count_objects(json_file, dirname) >= constants.FILE_LIMIT:
            json_file = str(int(json_file[0]) + 1) + '.json'
    with open(os.path.join(dirname + '/' + json_file), 'a+') as file:
        json.dump(obj, file, cls=CustomEncoder)
        file.write('\n')


def save_image(dirname, image_path, image_name):
    file_limit = constants.FILE_LIMIT
    if not os.path.isdir(dirname):
        make_directory(dirname)
    sub_dirs = os.listdir(dirname)
    if not sub_dirs:
        sub_dirs.append('1-' + str(file_limit))
        path = '1-' + str(file_limit)
        dirname = os.path.join(dirname, path)
        make_directory(dirname)
    else:
        if len(os.listdir(os.path.join(dirname + '/' + sorted(sub_dirs)[-1]))) >= file_limit:
            name = sorted(sub_dirs)[-1].split('-')
            name = str(int(name[0]) + file_limit) + '-' + str(int(name[1]) + file_limit)
            dirname = os.path.join(dirname + '/' + name)
            make_directory(dirname)
        else:
            dirname = os.path.join(dirname + '/' + sorted(sub_dirs)[-1])
    shutil.copy(image_path, os.path.join(dirname, image_name + '.jpg'))


def save(obj, dirname):  # save file pattern: save_xxxx.json
    filename = get_filename(dirname)
    with open(dirname + '/' + filename, 'a+') as file:
        json.dump(obj, file, cls=CustomEncoder)
        file.write('\n')  # add new line for next entries


def loadjson(file):
    """gets a file and deserializes line by line"""
    with open(file, 'r') as f:
        for line in f:
            yield json.loads(line)


def count_objects(filename, dirname):
    """returns number of objects in given file"""
    count = 0
    with open(dirname + '/' + filename, 'r') as f:
        for _ in f:
            count += 1
    return count


def get_json_files(dirname):
    """lists all JSON files in given directory"""
    try:
        return [f for f in os.listdir(dirname) if f.endswith('.json')]
    except FileNotFoundError:
        make_directory(dirname)


def get_filename(dirname):
    json_files = get_json_files(dirname)
    if not json_files:
        return '1.json'

    # check if number of objects exceeds limit of number of objects per file
    sorted_json_files = sorted(json_files, key=lambda x: int(x[0:-5]))
    if count_objects(sorted_json_files[-1], dirname) >= constants.FILE_LIMIT:
        return get_filename_pattern(sorted_json_files[-1])
    return sorted_json_files[-1]


def get_filename_pattern(filename):
    """returns next file pattern
     example: get save_25.json -> return save_26.json"""
    pattern = filename.rsplit('.')[0]
    pattern = str(int(pattern) + 1) + '.json'
    return pattern


def get_total(key, value, dirname):
    count = 0
    json_files = [f for f in os.listdir(dirname) if f.endswith('.json')]
    for filename in json_files:
        for dictionary in loadjson(dirname + '/' + filename):
            if dictionary[key] == value:
                count += 1
    return count


def search(obj_id, dirname):
    json_files = get_json_files(dirname)
    if not json_files:
        make_directory(dirname)
        json_files = get_json_files(dirname)
    for filename in json_files:
        for obj in loadjson(dirname + '/' + filename):
            if obj['id'] == obj_id:
                return obj


def get_all(dirname):
    object_list = []
    json_files = get_json_files(dirname)
    if not json_files:
        make_directory(dirname)
        json_files = get_json_files(dirname)
    for filename in json_files:
        for obj in loadjson(dirname + '/' + filename):
            object_list.append(obj)
    return object_list


def get_image(product_id, dirname):
    try:
        dirlist = [f for f in os.listdir(dirname)]
    except FileNotFoundError:
        make_directory(dirname)
        dirlist = []
    for directory in dirlist:
        image_list = os.listdir(os.path.join(dirname, directory))
        for image in image_list:
            image_name = image.split('.')[0]
            if image_name == str(product_id):
                return os.path.join(dirname, directory, image)


def find(key, value, dirname):
    json_files = get_json_files(dirname)
    if not json_files:
        make_directory(dirname)
        json_files = get_json_files(dirname)
    for filename in json_files:
        for obj in loadjson(dirname + '/' + filename):
            if obj[key] == value:
                return obj


def find_all(key, value, dirname):
    obj_list = []
    json_files = get_json_files(dirname)
    if not json_files:
        make_directory(dirname)
        json_files = get_json_files(dirname)
    for filename in json_files:
        for obj in loadjson(dirname + '/' + filename):
            if obj[key] == value:
                obj_list.append(obj)
    return obj_list


def search_phone(phone, dirname):
    json_files = get_json_files(dirname)
    if not json_files:
        make_directory(dirname)
        json_files = get_json_files(dirname)
    for filename in json_files:
        for obj in loadjson(dirname + '/' + filename):
            if obj['phone'] == phone:
                return obj


def random_products(category, count):
    dirname = constants.product_data_filepath()
    list_of_products = []
    json_files = get_json_files(dirname)
    if not json_files:
        make_directory(dirname)
        json_files = get_json_files(dirname)
    for filename in json_files:
        for obj in loadjson(dirname + '/' + filename):
            if obj['category'] == category and count > 0:
                list_of_products.append(obj)
                count -= 1
    return list_of_products


def get_next_id(dirname):
    json_files = get_json_files(dirname)
    if not json_files or os.stat(dirname + '/' + json_files[0]).st_size == 0:
        return 1
    for obj in loadjson(dirname + '/' + json_files[-1]):
        pass
    return int(obj['id']) + 1


def get_file(dirname, obj_id):
    json_files = get_json_files(dirname)
    for filename in json_files:
        for obj in loadjson(dirname + '/' + filename):
            if obj['id'] == obj_id:
                return filename


def overwrite(dirname, obj):
    if not isinstance(obj, dict):
        obj = beautify_all(obj)
    filename = get_file(dirname, obj['id'])
    object_list = []
    with open(dirname + '/' + filename, 'r+') as file:
        for line in file:
            if json.loads(line)['id'] == obj['id']:
                object_list.append(json.dumps(obj))
                continue
            object_list.append(line[:-1])
    with open(dirname + '/' + filename, 'w') as file:
        for item in object_list:
            file.write(item)
            file.write('\n')

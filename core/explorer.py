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


def save_cart(dirname, obj):
    if not os.path.isdir(dirname):
        make_directory(dirname)
    filename = get_filename(dirname)
    with open(os.path.join(dirname + '/' + filename), 'a+') as file:
        json.dump(obj, file, cls=CustomEncoder)
        file.write('\n')


def save_comment(dirname, obj):
    dirname += f'/product_{obj.product_id}'
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


def save_image(dirname, image, image_name):
    file_limit = constants.FILE_LIMIT
    if not os.path.isdir(dirname):
        make_directory(dirname)
    sub_dirs = os.listdir(dirname)
    if not sub_dirs:
        sub_dirs.append('1-' + str(file_limit))
        dirname = os.path.join(dirname + '/1-' + str(file_limit))
        make_directory(dirname)
    else:
        if len(os.listdir(os.path.join(dirname + '/' + sorted(sub_dirs)[-1]))) >= file_limit:
            name = sorted(sub_dirs)[-1].split('-')
            name = str(int(name[0]) + file_limit) + '-' + str(int(name[1]) + file_limit)
            dirname = os.path.join(dirname + '/' + name)
            make_directory(dirname)
        else:
            dirname = os.path.join(dirname + '/' + sorted(sub_dirs)[-1])

    shutil.copy(image, os.path.join(dirname, image_name))


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
        return 'save_0001.json'

    # check if number of objects exceeds limit of number of objects per file
    if count_objects(sorted(json_files)[-1], dirname) >= constants.FILE_LIMIT:
        return get_filename_pattern(json_files[-1])
    return json_files[-1]


def get_filename_pattern(filename):
    """returns next file pattern
     example: get save_0025.json -> return save_0026.json"""
    pattern = filename.rsplit('.')[0][-4:]
    pattern = 'save_' + (4 - len(str(int(pattern)))) * '0' + str(int(pattern) + 1) + '.json'
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
    for filename in json_files:
        for obj in loadjson(dirname + '/' + filename):
            if obj['id'] == obj_id:
                return obj


def get_next_id(dirname):
    json_files = get_json_files(dirname)
    if not json_files or os.stat(dirname + '/' + json_files[0]).st_size == 0:
        return '0001'
    for obj in loadjson(dirname + '/' + json_files[-1]):
        pass
    return (4 - len(str(int(obj['id'][-4:])))) * '0' + str(int(obj['id'][-4:]) + 1)


def get_file(dirname, obj_id):
    json_files = get_json_files(dirname)
    for filename in json_files:
        for obj in loadjson(dirname + '/' + filename):
            if obj['id'] == obj_id:
                return filename


def overwrite(dirname, obj):
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

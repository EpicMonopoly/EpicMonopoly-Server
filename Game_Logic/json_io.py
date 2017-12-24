import json
import os


def json_reader(file_name):
    """
    Read json
    :param file_name:
    :return:
    """
    if not os.path.isfile(file_name):
        raise IOError("JSON file {} does not exist.".format(file_name))
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def json_writer(file_name, data):
    """
    Write to json
    :param file_name:
    :param data:
    :return:
    """
    if not os.path.isfile(file_name):
        raise IOError("JSON file {} does not exist.".format(file_name))
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)


import json
import os


def json_reader(file_name):
    if not os.path.isfile(file_name):
        raise IOError("JSON file does not exist.")
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def json_writer(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    data = json_reader("bank_new.json")
    print(data)
    json_writer("bank_123.json",data)

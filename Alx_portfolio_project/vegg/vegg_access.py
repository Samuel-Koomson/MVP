import json

def data_read(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def data_write(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

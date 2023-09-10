import json


def parse_object(x):
    if x['short_desription'] is not None and 'name_ru' in x and 'poster_url' in x and 'description' in x:
        return True
    else:
        return False


def dump_json(file: str, data):
    otv = []
    for i in data:
        if parse_object(i):
            otv.append(i)

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(otv, f)


def start(file: str):
    f = open(file, encoding='utf-8')
    data = json.load(f)
    dump_json('Kinopois.json', data)

if __name__ == '__main__':
    start('KinopoiskDumb.json')
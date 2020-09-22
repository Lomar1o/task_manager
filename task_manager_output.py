import argparse
import os
from file import FileJson, FileSQL, convert_date


def to_string(data):
    # Конвертируем список в строку
    res = ''
    try:
        for key, value in data:
            res += f'{key} {", ".join(value)}\n'
    except TypeError:
        return res
    return res


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-date', type=str, help='Введите желаемую дату')
    args = parser.parse_args()

    # Если файла Json не существует, читаем из SQL
    if os.path.exists(FileJson().path_to_file):
        reader = FileJson()
    else:
        reader = FileSQL()

    args.date = convert_date(args.date)

    nxt, previous = reader.read_from_database(args.date)
    previous = to_string(previous)
    nxt = to_string(nxt)

    print(f'Предстоящие дела:\n{nxt}\n\nВыполненные дела:\n{previous}')


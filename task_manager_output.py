import argparse
import os
from file import FileJson, FileSQL, convert_date


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
    print(f'Предстоящие дела:\n{nxt}\n\nВыполненные дела:\n{previous}')


import argparse
<<<<<<< HEAD
from file import FileJson, FileSQL, convert_date
=======
# import os
# import json
from datetime import timedelta, date
from File import FileJson, FileSQL, get_date


def add_to_manager(task, _date, database=None):
    # Передаем на запись запланированную дату и занятие в виде словаря
    _date = convert_date(_date)
    dct = dict()
    dct[date] = task
    if args.database == 'SQL' or database is None:
        FileSQL(dct).add_to_datebase()
    elif args.database == 'Json':
        FileJson(dct).write_json()
    return f'Данные успешно занесены в журнал'


def convert_date(data):
    # Добавляем к введенной дате год
    day, month = get_date(data)
    d = date.today()
    if 'послезавтра' in data:
        d = d + timedelta(days=2)
    elif 'завтра' in data:
        d = d + timedelta(days=1)
    try:
        if d > d.replace(day=day, month=month, year=d.year):
            # Если дата уже прошла, то переходит на следующий год
            d = d.replace(day=day, month=month, year=d.year + 1)
        else:
            d = d.replace(day=day, month=month, year=d.year)
    except ValueError:
        raise ValueError('Введена неверная дата')
    return str(d)
>>>>>>> Task manager


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
<<<<<<< HEAD
    parser.add_argument('-task', type=str, help='Введите задание')
    parser.add_argument('-date', type=str, help='Введите дату')
    parser.add_argument('-database', help='Введите способ хранения данных:'\
                                          'SQL или Json. По умолчанию Json')
    args = parser.parse_args()

    print(args.date)
    args.date = convert_date(args.date)
    print(args.date)

    if args.database == 'Json' or not args.database:
        writer = FileJson()
    elif args.database == 'SQL':
        writer = FileSQL()
    print(args.date)
    writer.write(args.task, args.date)







#
#
# def add_to_manager(task, _date, database=None):
#     # Передаем на запись запланированную дату и занятие в виде словаря
#     _date = convert_date(_date)
#     dct = dict()
#     dct[date] = task
#     if args.database == 'SQL' or database is None:
#         FileSQL(dct).add_to_datebase()
#     elif args.database == 'Json':
#         FileJson(dct).write_json()
#     return f'Данные успешно занесены в журнал'
#
#
# def convert_date(data):
#     # Добавляем к введенной дате год
#     day, month = get_date(data)
#     d = date.today()
#     if 'послезавтра' in data:
#         d = d + timedelta(days=2)
#     elif 'завтра' in data:
#         d = d + timedelta(days=1)
#     try:
#         if d > d.replace(day=day, month=month, year=d.year):
#             # Если дата уже прошла, то переходит на следующий год
#             d = d.replace(day=day, month=month, year=d.year + 1)
#         else:
#             d = d.replace(day=day, month=month, year=d.year)
#     except ValueError:
#         raise ValueError('Введена неверная дата')
#     return str(d)
=======
    parser.add_argument('-task', type=str, help='enter task')
    parser.add_argument('-date', help='enter data')
    parser.add_argument('-database', help='Введите способ хранения данных:'\
                                          'SQL или Json. По умолчанию Json')
    args = parser.parse_args()
    add_to_manager(args.task, args.date, args.database)

>>>>>>> Task manager

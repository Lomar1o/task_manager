<<<<<<< HEAD
import argparse
import os
from file import FileJson, FileSQL, convert_date


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-date', type=str, help='Введите желаемую дату')
    args = parser.parse_args()

    if os.path.exists(FileJson().path_to_file):
        reader = FileJson()
    else:
        reader = FileSQL()

    args.date = convert_date(args.date)
    nxt, previous = reader.read(args.date)
    print(f'Предстоящие дела:\n{nxt}\n\nВыполненные дела:\n{previous}')








=======
import os
import argparse
from datetime import date
from File import FileJson, FileSQL, get_date


def read_from_json(data=None):
    today = convert_date(data)
    tasks = FileJson().read_json()
    sort_tasks = sorted(tasks.items(), key=lambda x: x[0])
    nxt = to_string([task for task in sort_tasks if str(today) < task[0]][:5])
    previous = to_string([task for task in sort_tasks if str(today) > task[0]][:5])
    return f'Предстоящие дела:\n{nxt}\n\nВыполненные дела:\n{previous}'


def read_from_sql(data=None):
    today = convert_date(data)
    tasks = FileSQL().read_from_database()
    nxt = '\n'.join([f'{key} {value}' for key, value in tasks.items() if str(today) < key][:5])
    previous = '\n'.join([f'{key} {value}' for key, value in tasks.items() if str(today) > key][:5])
    return f'Предстоящие дела:\n{nxt}\n\nВыполненные дела:\n{previous}'


def convert_date(data):
    today = date.today()
    try:
        if data is not None:
            day, month = get_date(data)
            today = today.replace(day=day, month=month, year=today.year)
            if today < date.today():
                today = today.replace(year=today.year + 1)
            return today
    except ValueError:
        raise ValueError('Введена неверная дата')


def to_string(data):
    res = ''
    for key, value in data:
        res += f'{key} {", ".join(value)}\n'
    return res


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-date', type=str, help='Введите желаемую дату')
    args = parser.parse_args()
    print(read_from_sql(args.date))
    print(read_from_json(args.date))
    if os.path.exists(FileJson().path_to_file):
        read_from_json(args.date)
    else:
        read_from_sql(args.date)
>>>>>>> Task manager





# next_tasks, previous_tasks = list(), list()
    # for date_task in sort_tasks:
    #     if str(today) < date_task[0]:
    #         next_tasks.append(date_task)
    #     elif str(today) > date_task[0]:
    #         previous_tasks.append(date_task)
    # next_tasks = from_dict_to_string(next_tasks)
    # previous_tasks = from_dict_to_string(previous_tasks)

    # next_tasks = OrderedDict(next_tasks)
    # for key, value in next_tasks.items():
    #     nxt += f'{key} {", ".join(value)}\n'
    # print(nxt)
    # next_tasks = list(map(lambda x: (x[0],', '.join(x[1])), next_tasks))
    # print(next_tasks)

    # for date_task in sort_tasks:
    #     if str(today) <= date_task[0]:
    #         date_index = sort_tasks.index(date_task) - 1
    # previous_tasks = sort_tasks[:date_index] if date_index <= 5 \
    #                 else sort_tasks[date_index-5:date_index]
    # next_tasks = sort_tasks[date_index:date_index+5] \
    #                 if len(sort_tasks) - date_index > 0 \
    #                 else sort_tasks[date_index:]
    # previous_tasks = OrderedDict(previous_tasks)

# def sort_data(today, tasks):
#     print(today, tasks)
#     nxt = [task for task in tasks if str(today) < task[0]]
#     previous = [task for task in tasks if str(today) > task[0]]
<<<<<<< HEAD
#     return nxt, previous

# def read_from_json(data=None):
#     today = convert_date(data)
#     tasks = FileJson().read_json()
#     sort_tasks = sorted(tasks.items(), key=lambda x: x[0])
#     nxt = to_string([task for task in sort_tasks if str(today) < task[0]][:5])
#     previous = to_string([task for task in sort_tasks if str(today) > task[0]][:5])
#     return f'Предстоящие дела:\n{nxt}\n\nВыполненные дела:\n{previous}'


# def read_from_sql(data=None):
#     today = convert_date(data)
#     tasks = FileSQL().read_from_database()
#     nxt = '\n'.join([f'{key} {value}' for key, value in tasks.items() if str(today) < key][:5])
#     previous = '\n'.join([f'{key} {value}' for key, value in tasks.items() if str(today) > key][:5])
#     return f'Предстоящие дела:\n{nxt}\n\nВыполненные дела:\n{previous}'

#
# def convert_date(data):
#     today = date.today()
#     try:
#         if data is not None:
#             day, month = get_date(data)
#             today = today.replace(day=day, month=month, year=today.year)
#             if today < date.today():
#                 today = today.replace(year=today.year + 1)
#             return today
#     except ValueError:
#         raise ValueError('Введена неверная дата')

#
# def to_string(data):
#     res = ''
#     for key, value in data:
#         res += f'{key} {", ".join(value)}\n'
#     return res
=======
#     return nxt, previous
>>>>>>> Task manager

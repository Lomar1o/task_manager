import os
import sqlite3
import json
import tempfile
from abc import ABC, abstractmethod
from datetime import timedelta, date


def convert_date(_date):
    # Добавляем к введенной дате год
    today = date.today()
    try:
        day, month = get_date(_date)
        if 'послезавтра' in _date:
            today = today + timedelta(days=2)
        elif 'завтра' in _date:
            today = today + timedelta(days=1)
    except AttributeError:
        return today
    try:
        if today > today.replace(day=day, month=month, year=today.year):
            # Если дата уже прошла, то переходит на следующий год
            today = today.replace(day=day, month=month, year=today.year + 1)
        else:
            today = today.replace(day=day, month=month, year=today.year)
    except ValueError:
        raise ValueError('Введена неверная дата')
    return str(today)

def get_date(_date):
    day, month = list(map(int, _date.split('.')))
    return day, month


class Base(ABC):

    def __init__(self):
        self.today = date.today()

    @abstractmethod
    def write(self, task, _date):
        pass

    @abstractmethod
    def read(self, _date=None):
        pass


class FileJson(Base):

    def __init__(self):
        self.path_to_file = os.path.join('', 'manager1.data')
        # self.path_to_file = os.path.join(tempfile.gettempdir(), 'manager.data')
        super().__init__()

    def write(self, task, _date):
        task = {_date: task}
        if os.path.exists(self.path_to_file):
            data = self._read_file()
        with open(self.path_to_file, 'w') as f:
            for key, value in task.items():
                if key not in data:
                    data[key] = list()
                data[key].append(value)
            json.dump(data, f)
        return f'Данные успешно занесены в журнал'

    def read(self, _date=None):
        tasks = self._read_file()
        sort_tasks = sorted(tasks.items(), key=lambda x: x[0])
        if _date is not None:
            self.today = _date
        nxt = self._to_string([task for task in sort_tasks \
                               if str(self.today) < task[0]][:5])
        previous = self._to_string([task for task in sort_tasks \
                                    if str(self.today) > task[0]][:-6:-1])
        return nxt, previous

    def _read_file(self):
        with open(self.path_to_file, 'r') as f:
            return json.load(f)

    def _to_string(self, data):
        res = ''
        try:
            for key, value in data:
                res += f'{key} {", ".join(value)}\n'
        except TypeError:
            return res
        return res


class FileSQL(Base):

    def __init__(self):
        self.conn = sqlite3.connect('database.db', uri=True)
        self.cursor = self.conn.cursor()
        super().__init__()

    def write(self, task, _date):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS manager
                               (date text, task text)''')
        data = _date, task
        self.cursor.execute('INSERT INTO manager VALUES(?,?)', data)
        self.conn.commit()
        self.conn.close()
        return f'Данные успешно занесены в журнал'

    def read(self, _date=None):
        if _date is not None:
            self.today = _date
        nxt = ''
        previous = ''
        try:
            for key, value in self.cursor.execute(
                    'SELECT date, task FROM manager \
                    WHERE date>:today ORDER BY date limit 0,5', \
                    {'today': self.today}):
                nxt += f'{key} {value}\n'
            for key, value in self.cursor.execute(
                    'SELECT date, task FROM manager \
                    WHERE date<:today ORDER BY date DESC limit 0,5',
                    {'today': self.today}):
                previous += f'{key} {value}\n'
        except sqlite3.OperationalError as err:
            raise sqlite3.OperationalError(
                            'В вашем планировщике еще нет записей', err
            )
        self.conn.close()
        # nxt = '\n'.join([f'{key} {value}' for key, value in res.items() if str(self.today) < key])
        # previous = '\n'.join([f'{key} {value}' for key, value in res.items() if str(self.today) > key])
        return nxt, previous





























# def convert_date(_date):
#     # Добавляем к введенной дате год
#     today = date.today()
#     try:
#         day, month = get_date(_date)
#         if 'послезавтра' in _date:
#             today = today + timedelta(days=2)
#         elif 'завтра' in _date:
#             today = today + timedelta(days=1)
#     except AttributeError:
#         return today
#     try:
#         if today > today.replace(day=day, month=month, year=today.year):
#             # Если дата уже прошла, то переходит на следующий год
#             today = today.replace(day=day, month=month, year=today.year + 1)
#         else:
#             today = today.replace(day=day, month=month, year=today.year)
#     except ValueError:
#         raise ValueError('Введена неверная дата')
#     return str(today)
#
#
# def get_date(_date):
#     day, month = list(map(int, _date.split('.')))
#     return day, month






# class Base(ABC):
#
#     def __init__(self, data=None):
#         self.data = data
#
#     @
#
#
#
# class FileJson:
#
#     def __init__(self, data=None):
#         # self.path_to_file = os.path.join(tempfile.gettempdir(), \
#         #                                  'manager1.data')
#         self.path_to_file = os.path.join('', 'manager1.data')
#         self.data = data
#         self.tasks = dict()
#
#     def write_json(self):
#         if os.path.exists(self.path_to_file):
#             self.tasks = self._read()
#         with open(self.path_to_file, 'w') as f:
#             for key, value in self.data.items():
#                 if key not in self.tasks:
#                     self.tasks[key] = list()
#                 self.tasks[key].append(value)
#             json.dump(self.tasks, f)
#         return f
#
#     def read_json(self):
#         if os.path.exists(self.path_to_file):
#             self.tasks = self._read()
#             return self.tasks
#         else:
#             raise FileNotFoundError('В вашем менеджере еще нет записей')
#
#     def _read(self):
#         with open(self.path_to_file, 'r') as f:
#             return json.load(f)
#
#
# def get_date(date):
#     day, month = list(map(int, date.split('.')))
#     return day, month
#
#
# class FileSQL:
#
#     def __init__(self, data=None):
#         self.data = data
#         self.conn = sqlite3.connect('database.db')
#         self.cursor = self.conn.cursor()
#
#     def add_to_datebase(self):
#         self.cursor.execute('''CREATE TABLE IF NOT EXISTS manager
#                                (date text, task text)''')
#         self.data = self.data.items()
#         self.cursor.executemany('INSERT INTO manager VALUES(?,?)', self.data)
#         self.conn.commit()
#
#     def read_from_database(self):
#         res = OrderedDict()
#         for key, value in self.cursor.execute('SELECT * FROM manager ORDER BY date'):
#             res[key] = value
#         return res
#
#
#

    # def convert_date(self, _date):
    #     # Добавляем к введенной дате год
    #     try:
    #         day, month = self.get_date(_date)
    #         if 'послезавтра' in _date:
    #             self.today = self.today + timedelta(days=2)
    #         elif 'завтра' in _date:
    #             self.today = self.today + timedelta(days=1)
    #     except AttributeError:
    #         return self.today
    #     try:
    #         if self.today > self.today.replace(day=day, month=month, year=self.today.year):
    #             # Если дата уже прошла, то переходит на следующий год
    #             self.today = self.today.replace(day=day, month=month, year=self.today.year + 1)
    #         else:
    #             self.today = self.today.replace(day=day, month=month, year=self.today.year)
    #     except ValueError:
    #         raise ValueError('Введена неверная дата')
    #     return str(self.today)

    # def get_date(self, _date):
    #     day, month = list(map(int, _date.split('.')))
    #     return day, month

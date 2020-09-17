import os
import sqlite3
import json
import tempfile
from abc import ABC, abstractmethod
from datetime import timedelta, date


def convert_date(_date):
    # Конвертируем полученную дату из дд.мм в гггг-мм-дд
    today = date.today()
    try:
        day, month = get_date(_date)
        if 'послезавтра' in _date:
            today = today + timedelta(days=2)
        elif 'завтра' in _date:
            today = today + timedelta(days=1)
    except AttributeError:
        return today
    # Если введенная дата прошла, то переносим ее на следующий год
    try:
        if today > today.replace(day=day, month=month, year=today.year):
            today = today.replace(day=day, month=month, year=today.year + 1)
        else:
            today = today.replace(day=day, month=month, year=today.year)
    except ValueError:
        raise ValueError('Введена неверная дата')
    return str(today)

def get_date(_date):
    # Из введенной даты получаем день и месяц в виде числа
    day, month = list(map(int, _date.split('.')))
    return day, month


class Base(ABC):
    """

    Абстрактный класс для создания общего интерфейся работы с БД.

    write_to_database() - записывает введенную пользователем информацию в БД,
    read_from_database() - читает информацию из БД.

    """
    def __init__(self):
        self.today = date.today()

    @abstractmethod
    def write_to_database(self, task, _date):
        pass

    @abstractmethod
    def read_from_database(self, _date=None):
        pass


class FileJson(Base):

    def __init__(self):
        # Задаем путь до файла, в котором хранится информация
        self.path_to_file = os.path.join(tempfile.gettempdir(), 'manager.data')
        super().__init__()

    def write_to_database(self, task, _date):
        task = {_date: task}
        # Читаем файл, если он не существует, создаем пустой словарь
        try:
            data = self._read_file()
        except json.JSONDecoderError:
            data = dict()
        # добавляем в словарь информацию {дата: [дело]}
        with open(self.path_to_file, 'w') as f:
            for key, value in task.items():
                if key not in data:
                    data[key] = list()
                data[key].append(value)
            json.dump(data, f)

    def read_from_database(self, _date=None):
        if _date is not None:
            self.today = _date
        tasks = self._read_file()
        # Сортируем, прочитанную из файла информацию, по дате
        sort_tasks = sorted(tasks.items(), key=lambda x: x[0])
        if _date is not None:
            self.today = _date
        # выбираем первые 5 предстоящие и выполненные дела
        nxt = self._to_string([task for task in sort_tasks \
                               if str(self.today) < task[0]][:5])
        previous = self._to_string([task for task in sort_tasks \
                                    if str(self.today) > task[0]][:-6:-1])
        return nxt, previous

    def _read_file(self):
        # Читаем из файла информацию
        with open(self.path_to_file, 'r') as f:
            return json.load(f)

    def _to_string(self, data):
        # Конвертируем список в строку
        res = ''
        try:
            for key, value in data:
                res += f'{key} {", ".join(value)}\n'
        except TypeError:
            return res
        return res


class FileSQL(Base):

    def __init__(self):
        # Устанавливаем соединение с БД
        self.conn = sqlite3.connect('database.db', uri=True)
        self.cursor = self.conn.cursor()
        super().__init__()

    def write_to_database(self, task, _date):
        # Создаем таблицу, если она не существует и вносим пользовательские данные.
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS manager
                               (date text, task text)''')
        data = _date, task
        self.cursor.execute('INSERT INTO manager VALUES(?,?)', data)
        self.conn.commit()
        self.conn.close()

    def read_from_database(self, _date=None):
        if _date is not None:
            self.today = _date
        nxt = ''
        previous = ''
        # Читаем из БД первые 5 выполненные и предстоящие задачи
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
        return nxt, previous



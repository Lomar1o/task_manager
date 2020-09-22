import os
import sqlite3
import json
import tempfile
from abc import ABC, abstractmethod
from datetime import timedelta, date


def convert_date(_date):
    # Конвертируем полученную дату из дд.мм в гггг-мм-дд
    if _date is None:
        return date.today()
    today = date.today()
    if _date == 'послезавтра':
        return today + timedelta(days=2)
    elif _date == 'завтра':
        return today + timedelta(days=1)
    # Если введенная дата прошла, то переносим ее на следующий год
    try:
        day, month = list(map(int, _date.split('.')))
        if today > today.replace(day=day, month=month, year=today.year):
            today = today.replace(day=day, month=month, year=today.year + 1)
        else:
            today = today.replace(day=day, month=month, year=today.year)
    except ValueError:
        raise ValueError('Введена неверная дата') from None
    return str(today)


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

    def sort_next_previous(self, data):
        # Сортируем, прочитанную из файла информацию, по дате
        sort_tasks = sorted(data.items(), key=lambda x: x[0])
        # выбираем первые 5 предстоящих и выполненных дела
        nxt = [task for task in sort_tasks if str(self.today) <= task[0]][:5]
        previous = [task for task in sort_tasks if str(self.today) > task[0]][:-6:-1]
        return nxt, previous


class FileJson(Base):

    def __init__(self):
        # Задаем путь до файла, в котором хранится информация
        # self.path_to_file = os.path.join(tempfile.gettempdir(), 'manager.data')
        self.path_to_file = os.path.join('', 'manager.data')
        super().__init__()

    def write_to_database(self, _date, task):
        # Читаем файл, если он не существует, создаем пустой словарь
        data = self._read_file()
        # добавляем в словарь информацию {дата: [дело]}
        with open(self.path_to_file, 'w') as f:
            data.setdefault(_date, []).append(task)
            json.dump(data, f)

    def read_from_database(self, _date=None):
        if _date is not None:
            self.today = _date
        tasks = self._read_file()
        nxt, previous = self.sort_next_previous(tasks)
        return nxt, previous

    def _read_file(self):
        # Читаем из файла информацию
        try:
            with open(self.path_to_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return dict()


class FileSQL(Base):

    def __init__(self):
        # Устанавливаем соединение с БД
        self.conn = sqlite3.connect('database.db', uri=True)
        self.cursor = self.conn.cursor()
        super().__init__()

    def write_to_database(self, _date, task):
        # Создаем таблицу, если она не существует и вносим пользовательские данные.
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS manager
                               (date text, task text)''')
        data = _date, task
        self.cursor.execute('INSERT INTO manager VALUES(?,?)', data)
        self.conn.commit()

    def read_from_database(self, _date=None):
        if _date is not None:
            self.today = _date
        data = dict()
        try:
            for key, value in self.cursor.execute(
                    'SELECT date, task FROM manager \
                     ORDER BY date', {'today': self.today}):
                data.setdefault(key, []).append(value)
        except sqlite3.OperationalError as err:
            raise sqlite3.OperationalError(
                    'В вашем планировщике еще нет записей', err
            )

        nxt, previous = self.sort_next_previous(data)
        return nxt, previous



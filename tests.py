import unittest
import sqlite3
import tempfile
import os
from random import randint
from datetime import timedelta, date
from file import FileSQL, FileJson, convert_date


class TestDate(unittest.TestCase):

    def test_not_valid_date(self):
        self.cases = (
            'abc', '24.13', '30.02', '55.22', '44.10', '28/03',
            'ac.ac', '03,02', '02.02.2020', '', '29.02', '01-01',
            '!@,@!', 'True', 'False', 'послепослезавтра', 'завтрак',
            'None'
        )

        for case in self.cases:
            with self.subTest(case=case):
                with self.assertRaises(ValueError):
                    convert_date(case)

    def test_valid_convert_date(self):
        today = date.today()
        self.cases = (
            ('01.01', '2021-01-01'), ('27.02', '2021-02-27'),
            ('10.10', '2020-10-10'), ('21.12', '2020-12-21'),
            ('завтра', today + timedelta(days=1)),
            ('послезавтра', today + timedelta(days=2))
        )

        for _date, result in self.cases:
            with self.subTest(_date=_date):
                self.assertEqual(convert_date(_date), result)


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.today = date.today()
        self.sql = FileSQL()
        self.sql.conn = sqlite3.connect(':memory:')
        self.json = FileJson()
        self.json.path_to_file = os.path.join(
                                tempfile.gettempdir(),
                                'manager1.data' + str(randint(1, 100))
        )

    def tearDown(self):
        self.sql.cursor.close()
        self.sql.conn.close()
        self.addCleanup(os.remove, self.json.path_to_file)

    def test_database_work(self):
        self.cases = (
            ('01.01', 'NewYear'), ('07.01', 'Christmas'),
            ('18.02', 'test_case'), ('09.09', 'test_case_2'),
            ('07.06', 'test_case_3'), ('22.05', 'test_case_4'),
            ('17.07', 'test_case_5'), ('21.12', 'test_case_6'),
            ('23.10', 'test_case_7'), ('07.01', 'OldYear'),
            ('18.02', 'test_case_8'), ('18.02', 'test_case_9'),
            ('09.10', 'test_case_10'), ('11.11', 'test_case_11')
        )
        self.result = (
            ('22.09', ([('2020-10-09', ['test_case_10']),
                         ('2020-10-23', ['test_case_7']),
                         ('2020-11-11', ['test_case_11']),
                         ('2020-12-21', ['test_case_6']),
                         ('2021-01-01', ['NewYear'])],
                         []
                       )),
            ('31.01',
                      ([('2021-02-18', ['test_case', 'test_case_8', 'test_case_9']),
                        ('2021-05-22', ['test_case_4']), ('2021-06-07', ['test_case_3']),
                        ('2021-07-17', ['test_case_5']), ('2021-09-09', ['test_case_2'])],
                       [('2021-01-07', ['Christmas', 'OldYear']), ('2021-01-01', ['NewYear']),
                        ('2020-12-21', ['test_case_6']), ('2020-11-11', ['test_case_11']),
                        ('2020-10-23', ['test_case_7'])])),
            ('21.09', ([],
                       [('2021-09-09', ['test_case_2']), ('2021-07-17', ['test_case_5']),
                        ('2021-06-07', ['test_case_3']), ('2021-05-22', ['test_case_4']),
                        ('2021-02-18', ['test_case', 'test_case_8', 'test_case_9'])]))
            )

        for case in self.cases:
            with self.subTest(case=case):
                self.sql.write_to_database(convert_date(case[0]), case[1])
                self.json.write_to_database(convert_date(case[0]), case[1])

        for _date, res in self.result:
            with self.subTest(_date=_date):
                self.assertEqual(
                    self.json.read_from_database(convert_date(_date)),
                    res
                )
                self.assertEqual(
                    self.json.read_from_database(convert_date(_date)),
                    self.sql.read_from_database(convert_date(_date))
                )


if __name__ == '__main__':
    unittest.main()

import argparse
from file import FileJson, FileSQL, convert_date
from file import FileJson, FileSQL


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-task', type=str, help='Введите задание')
    parser.add_argument('-date', type=str, help='Введите дату')
    parser.add_argument('-database', help='Введите способ хранения данных:'\
                                          'SQL или Json. По умолчанию Json')
    args = parser.parse_args()

    # Конвертируем дату из дд.мм в гггг.мм.дд
    args.date = convert_date(args.date)

    # В зависимости от пользовательского ввода, выбираем, где хранить данные
    if args.database == 'Json' or not args.database:
        writer = FileJson()
        print(f'Данные успешно занесены в журнал')
    elif args.database == 'SQL':
        writer = FileSQL()
        print(f'Данные успешно занесены в журнал')
    writer.write_to_database(args.task, args.date)


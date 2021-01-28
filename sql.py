import sqlite3
from prettytable import PrettyTable


class SQL:

    def __init__(self, database):
        """Подключение к БД"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже пользователь в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM "subscriptions" WHERE "user_id" = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, first_name, username):
        """Добавляем нового пользователя"""
        with self.connection:
            return self.cursor.execute("INSERT INTO 'subscriptions' ('user_id', 'first_name', 'username') VALUES(?,?,?)", (user_id, first_name, username))

    def add_count_graph(self, user_id):
        """Увеличиваем счетчик запросов графика"""
        with self.connection:
            return self.cursor.execute("UPDATE 'subscriptions' SET count_graph = count_graph + 1 WHERE user_id = ?", (user_id,))

    def add_count_list(self, user_id):
        """Увеличиваем счетчик запросов листов"""
        with self.connection:
            return self.cursor.execute("UPDATE 'subscriptions' SET count_list = count_list + 1 WHERE user_id = ?", (user_id,))

    def add_count_date_file(self, user_id):
        """Увеличиваем счетчик запросов даты файла"""
        with self.connection:
            return self.cursor.execute("UPDATE 'subscriptions' SET date_file = date_file + 1 WHERE user_id = ?", (user_id,))

    def read_bd(self):
        """Вывод информации с БД в чат"""
        with self.connection:
            data = self.cursor.execute('SELECT * FROM "subscriptions"').fetchall()
            table = PrettyTable()
            for item in data:
                table.field_names = ['ID', 'Name', 'Username', 'Graph', 'List', 'Date']
                table.add_row([item[0], item[1], item[2], item[3], item[4], item[5]])
            return f'```{table}```'

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()

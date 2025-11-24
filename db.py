from mysql.connector import Error
from config import config as config_module
import os

config = config_module.load_db_config()


def create_database_if_not_exists(config):
    """Створення бази даних, якщо вона не існує, без підключення до конкретної БД."""
    config_without_db = config.copy()
    config_without_db.pop("database", None)

    connection = config_module.wait_for_db(config_without_db)

    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS `online-banking-db`")
    print("База даних створена або вже існує.")
    cursor.close()
    connection.close()


def execute_sql_file(connection, sql_file_path):
    cursor = connection.cursor()
    if not os.path.exists(sql_file_path):
        print(f"Файл {sql_file_path} не знайдено!")
        return
    with open(sql_file_path, "r", encoding="utf-8") as f:
        sql_commands = f.read().split(';')
        for command in sql_commands:
            command = command.strip()
            if command:
                try:
                    cursor.execute(command)
                except Error as e:
                    print(f"Помилка виконання команди:\n{command}\n{e}")
    connection.commit()
    cursor.close()
    print(f"SQL-файл {sql_file_path} виконано успішно!")


def main():
    create_database_if_not_exists(config)

    db_config_with_name = config.copy()
    db_config_with_name['database'] = 'online-banking-db'

    connection = config_module.wait_for_db(db_config_with_name)

    execute_sql_file(connection, "scenary.sql")

    connection.close()


if __name__ == "__main__":
    main()
import click         # Бібліотека для створення CLI (Command Line Interface)
import pandas as pd  # Для роботи з CSV-файлами у вигляді таблиць (DataFrame)

# 🔍 Перевірка: чи є символи переносу рядка (\r\n) всередині клітинок
def carriage_returns(df):
    for index, row in df.iterrows():  # проходимо по кожному рядку
        for column, field in row.items():  # по кожному полю в рядку (оновлено для pandas 2.0+)
            try:
                if "\r\n" in field:  # якщо вміст клітинки містить перенос
                    return index, column, field  # повертаємо позицію та сам текст
            except TypeError:
                continue  # пропускаємо значення, які не є рядками

# 🔍 Перевірка: рахує кількість колонок з назвою "Unnamed"
def unnamed_columns(df):
    bad_columns = []
    for key in df.keys():
        if "Unnamed" in key:  # pandas створює такі назви, якщо в CSV відсутній заголовок
            bad_columns.append(key)
    return len(bad_columns)  # повертає кількість таких колонок

# 🔍 Перевірка: знаходить колонки, в яких немає жодного значення
def zero_count_columns(df):
    bad_columns = []
    for key in df.keys():
        if df[key].count() == 0:  # count() рахує непорожні значення
            bad_columns.append(key)
    return bad_columns

# ⚙️ Основна команда 'check' — приймає CSV-файл і запускає всі перевірки
@click.command()
@click.argument('filename', type=click.Path(exists=True))  # шлях до файлу
def check(filename):
    df = pd.read_csv(filename)  # зчитуємо CSV у вигляді таблиці

    # 🚨 Перевірка: порожні колонки
    for column in zero_count_columns(df):
        click.echo(f"Warning: Column '{column}' has no items in it")

    # 🚨 Перевірка: колонка з назвою Unnamed
    unnamed = unnamed_columns(df)
    if unnamed:
        click.echo(f"Warning: found {unnamed} columns that are Unnamed")

    # 🚨 Перевірка: символи переносу рядка всередині клітинок
    carriage_field = carriage_returns(df)
    if carriage_field:
        index, column, field = carriage_field
        click.echo((f"Warning: found carriage returns at index {index}"
                    f" of column '{column}':"))
        click.echo(f"         '{field[:50]}'")  # виводимо перші 50 символів

# 🔔 Додаткова команда — просто привітання (демо CLI)
@click.command()
@click.option("--name", default="світ", help="Ім’я користувача")
def hello(name):
    click.echo(f"Привіт, {name}!")

# 🧩 Оголошуємо CLI-групу, щоб мати кілька команд
@click.group()
def cli():
    pass

# ➕ Реєструємо команди в CLI
cli.add_command(hello)
cli.add_command(check)

# ▶️ Запускаємо CLI при виклику скрипту напряму
if __name__ == '__main__':
    cli()

#python csv_linter/main.py hello --name Maksym
#python csv_linter/main.py check test.csv

#.\cli-linter.exe hello --name Maksym
#.\cli-linter.exe check test.csv

import sys
import os
import pandas as pd

# 🔧 Додаємо папку csv_linter у шлях, щоб імпортувати з неї модуль
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'csv_linter')))

# Тепер можемо імпортувати функції напряму
from main import (
    zero_count_columns,
    unnamed_columns,
    carriage_returns
)


# 🔍 Тестуємо: чи правильно виявляється колонка без значень
def test_zero_count_columns():
    df = pd.DataFrame({
        'A': [1, 2],
        'B': [None, None],
        'C': ['x', 'y']
    })
    result = zero_count_columns(df)
    assert result == ['B']


# 🔍 Тестуємо: чи рахує кількість колонок з назвою "Unnamed"
def test_unnamed_columns():
    df = pd.DataFrame([[1, 2, 3]], columns=['A', 'Unnamed: 1', 'C'])
    result = unnamed_columns(df)
    assert result == 1


# 🔍 Тестуємо: чи знаходиться перенос рядка \r\n у клітинці
def test_carriage_returns_found():
    df = pd.DataFrame({
        'A': ['рядок 1\r\nрядок 2'],
        'B': ['ok']
    })
    result = carriage_returns(df)
    assert result == (0, 'A', 'рядок 1\r\nрядок 2')


# 🔍 Тестуємо: якщо переносів нема — функція має повернути None
def test_carriage_returns_not_found():
    df = pd.DataFrame({
        'A': ['звичайний текст'],
        'B': ['ще щось']
    })
    result = carriage_returns(df)
    assert result is None

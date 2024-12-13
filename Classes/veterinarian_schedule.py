import pandas as pd
import os


def load_veterinarian_schedule(filename: str):
    # Проверяем, существует ли файл по указанному пути
    if not os.path.exists(filename):
        # Если файл не найден, выбрасываем исключение с сообщением об ошибке
        raise FileNotFoundError(f"Файл '{filename}' не найден.")  # Проверка на существование файла

    # Загружаем данные из Excel-файла в DataFrame с помощью pandas
    schedule_df = pd.read_excel(filename)  # Загружаем данные из Excel
    # Возвращаем DataFrame, содержащий расписание ветеринаров
    return schedule_df  # Возвращаем DataFrame с расписанием


def select_veterinarian(schedule_df):
    # Запрашиваем у пользователя выбор ветеринара
    print("Выберите ветеринара:")
    # Перебираем строки DataFrame и выводим имена ветеринаров с их индексами
    for index, row in schedule_df.iterrows():
        print(f"{index + 1}: {row['Veterinarian Name']}")  # Выводим список ветеринаров

    # Получаем выбор пользователя и уменьшаем его на 1 для соответствия индексу DataFrame
    choice = int(input("Введите номер ветеринара: ")) - 1  # Получаем выбор пользователя
    # Возвращаем имя выбранного ветеринара из DataFrame
    return schedule_df.iloc[choice]['Veterinarian Name']  # Возвращаем имя выбранного ветеринара
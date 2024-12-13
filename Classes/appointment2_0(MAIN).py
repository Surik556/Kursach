from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication
from clinic import Clinic
from registration_window import AppointmentRegistrationWindow
from veterinarian_schedule import load_veterinarian_schedule

# Основная функция для запуска приложения
def main():
    app = QApplication([])  # Создаем экземпляр приложения

    # Загружаем расписание ветеринаров из файла
    schedule_df = load_veterinarian_schedule('Classes_for_veterinars/veterinarian_schedule.xlsx')  # Замените на ваш файл
    veterinarians = schedule_df[['Имя', 'Фамилия']].apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1).tolist()  # Получаем список ветеринаров с именем и фамилией

    clinic = Clinic()  # Создаем экземпляр клиники
    window = AppointmentRegistrationWindow(clinic, veterinarians)  # Создаем окно регистрации
    window.show()  # Показываем окно

    app.exec()  # Запускаем главный цикл приложения

# Точка входа в программу
if __name__ == "__main__":
    main()  # Запускаем основную функцию
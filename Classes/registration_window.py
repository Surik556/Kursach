from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
from client import Client
from animal import Animal
from appointment import Appointment
from clinic import Clinic
from ticket import create_ticket_image, open_ticket


class AppointmentRegistrationWindow(QMainWindow):
    def __init__(self, clinic: Clinic, veterinarians: list):
        super().__init__()
        self.clinic = clinic  # Ссылка на объект клиники
        self.veterinarians = veterinarians  # Список ветеринаров
        self.setWindowTitle("Регистрация на прием")  # Заголовок окна
        self.setGeometry(100, 100, 400, 400)  # Размеры окна

        self.layout = QVBoxLayout()  # Вертикальный компоновщик для размещения виджетов

        # Поле ввода для имени владельца
        self.owner_name_input = QLineEdit(self)
        self.owner_name_input.setPlaceholderText("Введите ФИО клиента")  # Подсказка для пользователя
        self.layout.addWidget(self.owner_name_input)  # Добавляем поле в компоновщик

        # Поле ввода для телефона владельца
        self.owner_phone_input = QLineEdit(self)
        self.owner_phone_input.setPlaceholderText("Введите телефон клиента")  # Подсказка для пользователя
        self.layout.addWidget(self.owner_phone_input)  # Добавляем поле в компоновщик

        # Поле ввода для email владельца
        self.owner_email_input = QLineEdit(self)
        self.owner_email_input.setPlaceholderText("Введите email клиента")  # Подсказка для пользователя
        self.layout.addWidget(self.owner_email_input)  # Добавляем поле в компоновщик

        # Поле ввода для имени животного
        self.animal_name_input = QLineEdit(self)
        self.animal_name_input.setPlaceholderText("Введите имя животного")  # Подсказка для пользователя
        self.layout.addWidget(self.animal_name_input)  # Добавляем поле в компоновщик

        # Поле ввода для вида животного
        self.animal_species_input = QLineEdit(self)
        self.animal_species_input.setPlaceholderText("Введите вид животного")  # Подсказка для пользователя
        self.layout.addWidget(self.animal_species_input)  # Добавляем поле в компоновщик

        # Поле ввода для породы животного
        self.animal_breed_input = QLineEdit(self)
        self.animal_breed_input.setPlaceholderText("Введите породу животного")  # Подсказка для пользователя
        self.layout.addWidget(self.animal_breed_input)  # Добавляем поле в компоновщик

        # Поле ввода для возраста животного
        self.animal_age_input = QLineEdit(self)
        self.animal_age_input.setPlaceholderText("Введите возраст животного (в годах)")  # Подсказка для пользователя
        self.layout.addWidget(self.animal_age_input)  # Добавляем поле в компоновщик

        # Поле ввода для даты приема
        self.appointment_date_input = QLineEdit(self)
        self.appointment_date_input.setPlaceholderText("Введите дату приема (ГГГГ-ММ-ДД)")  # Подсказка для пользователя
        self.layout.addWidget(self.appointment_date_input)  # Добавляем поле в компоновщик

        # Комбобокс для выбора дня недели
        self.appointment_date_combo = QComboBox(self)
        self.appointment_date_combo.addItems(["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"])  # Выбор дня недели
        self.layout.addWidget(self.appointment_date_combo)  # Добавляем комбобокс в компоновщик

        # Комбобокс для выбора времени приема
        self.appointment_time_combo = QComboBox(self)
        self.appointment_time_combo.addItems(["Утро", "День", "Вечер"])  # Выбор времени
        self.layout.addWidget(self.appointment_time_combo)  # Добавляем комбобокс в компоновщик

        # Комбобокс для выбора ветеринара
        self.veterinarian_combo = QComboBox(self)
        self.veterinarian_combo.addItems([str(vet) for vet in self.veterinarians])  # Преобразуем список ветеринаров в строки
        self.layout.addWidget(self.veterinarian_combo)  # Добавляем комбобокс в компоновщик

        # Кнопка для добавления записи
        self.submit_button = QPushButton("Добавить запись", self)
        self.submit_button.clicked.connect(self.add_appointment)  # Подключаем метод добавления записи к кнопке
        self.layout.addWidget(self.submit_button)  # Добавляем кнопку в компоновщик

        # Создаем контейнер для компоновки и устанавливаем его как центральный виджет
        container = QWidget()  # Создаем контейнер для компоновки
        container.setLayout(self.layout)  # Устанавливаем компоновщик
        self.setCentralWidget(container)  # Устанавливаем центральный виджет

    def add_appointment(self):
        # Получаем данные из полей ввода
        owner_name = self.owner_name_input.text().strip()  # Имя владельца
        owner_phone = self.owner_phone_input.text().strip()  # Телефон владельца
        owner_email = self.owner_email_input.text().strip()  # Email владельца
        animal_name = self.animal_name_input.text().strip()  # Имя животного
        animal_species = self.animal_species_input.text().strip()  # Вид животного
        animal_breed = self.animal_breed_input.text().strip()  # Порода животного
        animal_age = self.animal_age_input.text().strip()  # Возраст животного
        appointment_date = self.appointment_date_combo.currentText()  # Получаем выбранный день недели
        appointment_time = self.appointment_time_combo.currentText()  # Получаем выбранное время

        # Проверяем, заполнены ли все поля
        if not owner_name or not owner_phone or not owner_email or not animal_name or not animal_species or not animal_breed or not animal_age or not appointment_date or not appointment_time:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")  # Сообщение об ошибке
            return

        # Проверяем корректность возраста животного
        try:
            animal_age = int(animal_age)  # Преобразуем возраст в целое число
            if animal_age < 0:
                raise ValueError("Возраст не может быть отрицательным.")  # Проверка на отрицательный возраст
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Возраст должен быть положительным числом.")  # Сообщение об ошибке
            return

        # Создаем экземпляры клиента и животного
        client_instance = Client(owner_name, owner_phone, owner_email)  # Создаем объект клиента
        animal = Animal(animal_name, animal_species, animal_breed, animal_age)  # Создаем объект животного
        appointment = Appointment(animal, client_instance, appointment_date, appointment_time)  # Создаем объект записи

        # Добавляем запись в клинику
        self.clinic.add_appointment(appointment)  # Добавляем запись в клинику
        QMessageBox.information(self, "Успех", "Запись успешно добавлена!")  # Успешное сообщение

        # Сохраняем записи в файл
        filename = 'appointments.docx'  # Имя файла для сохранения
        veterinarian_name = self.veterinarian_combo.currentText()  # Получаем имя выбранного ветеринара
        file_path = self.clinic.save_to_docx(filename, veterinarian_name)  # Сохраняем записи и получаем путь к файлу
        QMessageBox.information(self, "Успех",
                                "Записи успешно сохранены в файл appointments.docx")  # Успешное сообщение

        self.clear_inputs()  # Очищаем поля ввода

        # Создаем и открываем изображение талона
        ticket_image_path = f'tickets/ticket_{animal.name}_{appointment_date}.png'  # Путь к изображению талона
        create_ticket_image(appointment, ticket_image_path)  # Создаем изображение

        open_ticket(ticket_image_path)  # Открываем талон

    def clear_inputs(self):
        # Очищаем все поля ввода
        self.owner_name_input.clear()  # Очищаем поле имени владельца
        self.owner_phone_input.clear()  # Очищаем поле телефона владельца
        self.owner_email_input.clear()  # Очищаем поле email владельца
        self.animal_name_input.clear()  # Очищаем поле имени животного
        self.animal_species_input.clear()  # Очищаем поле вида животного
        self.animal_breed_input.clear()  # Очищаем поле породы животного
        self.animal_age_input.clear()  # Очищаем поле возраста животного
        self.appointment_date_input.clear()  # Очищаем поле даты приема
        self.appointment_time_combo.clear()  # Очищаем комбобокс времени приема
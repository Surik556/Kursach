import os
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton, QMessageBox, QDialog, QLineEdit
from docx import Document
import pandas as pd
from datetime import datetime

class VeterinarianSelectionDialog(QDialog):
    def __init__(self, veterinarians):
        super().__init__()
        self.setWindowTitle("Выбор ветеринара")
        self.layout = QVBoxLayout()
        
        self.vet_combo = QComboBox(self)
        self.vet_combo.addItems(veterinarians)
        self.layout.addWidget(self.vet_combo)

        self.select_button = QPushButton("Выбрать", self)
        self.select_button.clicked.connect(self.accept)
        self.layout.addWidget(self.select_button)

        self.setLayout(self.layout)

    def get_selected_veterinarian(self):
        return self.vet_combo.currentText()

class AppointmentViewer(QMainWindow):
    def __init__(self, veterinarian_name):
        super().__init__()
        self.setWindowTitle(f"Записи для {veterinarian_name}")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()
        self.appointment_label = QLabel("Записи на прием:", self)
        self.layout.addWidget(self.appointment_label)

        self.appointment_list = QComboBox(self)
        self.layout.addWidget(self.appointment_list)

        self.date_input = QLineEdit(self)
        self.date_input.setPlaceholderText("Введите дату (YYYY-MM-DD)")
        self.layout.addWidget(self.date_input)

        self.search_button = QPushButton("Поиск по дате", self)
        self.search_button.clicked.connect(self.search_appointments)
        self.layout.addWidget(self.search_button)

        self.delete_button = QPushButton("Удалить запись", self)
        self.delete_button.clicked.connect(self.delete_appointment)
        self.layout.addWidget(self.delete_button)

        self.load_appointments(veterinarian_name)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def search_appointments(self):
        date_str = self.date_input.text()
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                self.load_appointments(self.vet_combo.currentText(), date_obj)
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Неверный формат даты. Используйте YYYY-MM-DD.")

    def load_appointments(self, veterinarian_name, filter_date=None):
        appointments = []
        directory = 'appointment_for_vet'
        print(f"Ищем записи для ветеринара: {veterinarian_name}")  # Отладочное сообщение
        
        # Формируем имя файла на основе фамилии и имени ветеринара
        veterinarian_filename = veterinarian_name.replace(" ", "_")  # Заменяем пробелы на подчеркивания для имени файла
        
        for filename in os.listdir(directory):
            if filename.startswith(veterinarian_filename) and filename.endswith('.docx'):
                print(f"Обрабатываем файл: {filename}")  # Отладочное сообщение
                doc = Document(os.path.join(directory, filename))
                for para in doc.paragraphs:
                    appointment_details = para.text.split(', ')  # Split by comma
                    if len(appointment_details) > 4:  # Ensure there are enough details
                        date_str = appointment_details[4].split(': ')[1]  # Extract date
                        print(f"Найдена строка: {para.text}")  # Отладочное сообщение
                        if date_str and date_str != '0':  # Ensure it's not empty or '0'
                            try:
                                date_obj = datetime.strptime(date_str, "%Y-%m-%d")  # Convert to datetime
                                if filter_date is None or date_obj.date() == filter_date.date():
                                    appointments.append((date_obj, para.text))  # Store as tuple (date, details)
                            except ValueError:
                                print(f"Неверный формат даты для записи: {para.text}")  # Log invalid date
                        else:
                            print(f"Нет действительной даты в записи: {para.text}")  # Log missing date

        # Sort appointments by date
        appointments.sort(key=lambda x: x[0])  # Sort by the date object

        if appointments:
            self.appointment_list.clear()
            for appt in appointments:
                self.appointment_list.addItem(appt[1])
        else:
            self.appointment_list.addItem("Нет записей для выбранного ветеринара.")

    def delete_appointment(self):
        selected_appointment = self.appointment_list.currentText()
        if selected_appointment and selected_appointment != "Нет записей для выбранного ветеринара.":
            print(f"Удаляем запись: {selected_appointment}")  # Отладочное сообщение
            self.load_appointments(self.vet_combo.currentText())  # Обновить список после удаления
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите запись для удаления.")

def load_veterinarian_schedule(filename: str):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл '{filename}' не найден.")
    
    schedule_df = pd.read_excel(filename)
    print("Columns in the schedule DataFrame:", schedule_df.columns.tolist())  # Debugging line
    return schedule_df['Фамилия'].tolist()

def main():
    app = QApplication([])
    
    # Загрузите расписание ветеринаров из файла
    veterinarians = load_veterinarian_schedule('veterinarian_schedule.xlsx')

    # Открытие диалога выбора ветеринара
    dialog = VeterinarianSelectionDialog(veterinarians)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        selected_veterinarian = dialog.get_selected_veterinarian()
        viewer_window = AppointmentViewer(selected_veterinarian)
        viewer_window.show()
        app.exec()

if __name__ == "__main__":
    main()

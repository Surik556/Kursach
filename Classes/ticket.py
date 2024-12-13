import subprocess
from PIL import Image, ImageDraw, ImageFont
from appointment import Appointment
import os

def create_ticket_image(appointment: Appointment, file_path: str):
    # Создаем новое изображение размером 400x300 пикселей с белым фоном
    img = Image.new('RGB', (400, 300), color='white')
    d = ImageDraw.Draw(img)  # Создаем объект для рисования на изображении
    font = ImageFont.load_default()  # Загружаем шрифт по умолчанию

    # Добавляем текст на изображение с информацией о записи
    d.text((10, 10), f"Талон на прием", fill=(0, 0, 0), font=font)  # Заголовок
    d.text((10, 50), f"Клиент: {appointment.client.name}", fill=(0, 0, 0), font=font)  # Имя клиента
    d.text((10, 70), f"Телефон: {appointment.client.phone}", fill=(0, 0, 0), font=font)  # Телефон клиента
    d.text((10, 90), f"Email: {appointment.client.email}", fill=(0, 0, 0), font=font)  # Email клиента
    d.text((10, 110), f"Животное: {appointment.animal.name}", fill=(0, 0, 0), font=font)  # Имя животного
    d.text((10, 130), f"Дата: {appointment.date}", fill=(0, 0, 0), font=font)  # Дата записи
    d.text((10, 150), f"Время: {appointment.time}", fill=(0, 0, 0), font=font)  # Время записи
    d.text((10, 170), f"Пожалуйста, не опаздывайте", fill=(0, 0, 0), font=font)  # Напоминание о времени

    # Проверяем, существует ли директория для сохранения билетов, если нет, создаем ее
    directory = 'Tickets'
    if not os.path.exists(directory):
        os.makedirs(directory)  # Создаем директорию

    img.save(file_path)  # Сохраняем изображение по указанному пути

def open_ticket(file_path):
    # Открываем файл с билетом с помощью системной команды
    subprocess.run(['open', file_path])  # Для macOS
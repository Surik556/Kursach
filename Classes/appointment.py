from animal import Animal
from client import Client

class Appointment:
    def __init__(self, animal: Animal, client: Client, date: str, time: str):
        self.animal = animal  # Животное, связанное с записью
        self.client = client  # Клиент, связанный с записью
        self.date = date  # Дата приема
        self.time = time  # Время приема
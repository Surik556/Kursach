import sqlite3  # or another database library

# Establish a connection to the database
conn = sqlite3.connect('clinic.db')  # Change to your database file or connection string
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE Veterinarians (
    veterinarian_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialization TEXT,
    phone TEXT,
    email TEXT
);
''')

cursor.execute('''
CREATE TABLE Clients (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT
);
''')

cursor.execute('''
CREATE TABLE Animals (
    animal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    species TEXT,
    breed TEXT,
    age INTEGER,
    client_id INTEGER,
    FOREIGN KEY (client_id) REFERENCES Clients(client_id)
);
''')

cursor.execute('''
CREATE TABLE Appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    animal_id INTEGER,
    veterinarian_id INTEGER,
    date DATE NOT NULL,
    time TIME NOT NULL,
    FOREIGN KEY (animal_id) REFERENCES Animals(animal_id),
    FOREIGN KEY (veterinarian_id) REFERENCES Veterinarians(veterinarian_id)
);
''')

# Commit changes and close the connection
conn.commit()
conn.close()

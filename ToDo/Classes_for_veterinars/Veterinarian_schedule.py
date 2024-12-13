import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QMessageBox, QComboBox
from PyQt6.QtCore import Qt

class TableEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Редактор таблицы")
        self.setGeometry(100, 100, 800, 400)

        self.table_widget = QTableWidget(0, 8)
        self.table_widget.setHorizontalHeaderLabels(["Фамилия", "Имя", "Отчество", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница"])
        self.table_widget.setStyleSheet("QTableWidget { border: 1px solid #ccc; background-color: white; color: black; }"
                                         "QHeaderView::section { background-color: #f0f0f0; font-weight: bold; }"
                                         "QTableWidget::item { padding: 5px; }")

        self.load_data()  # Загрузка данных из Excel при запуске

        self.save_button = QPushButton("Сохранить изменения")
        self.save_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 10px; border: none; border-radius: 5px; }"
                                        "QPushButton:hover { background-color: #45a049; }")
        self.save_button.clicked.connect(self.save_data)

        self.add_row_button = QPushButton("Добавить строку")
        self.add_row_button.setStyleSheet("QPushButton { background-color: #2196F3; color: white; padding: 10px; border: none; border-radius: 5px; }"
                                           "QPushButton:hover { background-color: #1E88E5; }")
        self.add_row_button.clicked.connect(self.add_row)

        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addWidget(self.add_row_button)
        layout.addWidget(self.save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_data(self):
        try:
            df = pd.read_excel("veterinarian_schedule.xlsx")  # Загрузка данных из Excel
            self.table_widget.setRowCount(len(df))  # Установка количества строк
            for row in range(len(df)):
                for column in range(len(df.columns)):
                    if column >= 3:  # Для столбцов дней недели
                        combo = QComboBox()
                        combo.addItems(["", "Утро", "День", "Вечер"])  # Примеры значений
                        combo.setCurrentText(str(df.iat[row, column]))  # Установка текущего значения
                        combo.setStyleSheet("QComboBox { color: black; }")  # Установка черного цвета текста
                        self.table_widget.setCellWidget(row, column, combo)  # Установка QComboBox в ячейку
                    else:
                        item = QTableWidgetItem(str(df.iat[row, column]))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.table_widget.setItem(row, column, item)
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", "Файл veterinarian_schedule.xlsx не найден. Начинаем с пустой таблицы.")

    def add_row(self):
        row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(row_count)  # Добавление новой строки
        for column in range(8):
            if column >= 3:  # Для столбцов дней недели
                combo = QComboBox()
                combo.addItems(["", "Утро", "День", "Вечер"])  # Примеры значений
                combo.setStyleSheet("QComboBox { color: Whith; }")  # Установка черного цвета текста
                self.table_widget.setCellWidget(row_count, column, combo)  # Установка QComboBox в ячейку
            else:
                item = QTableWidgetItem("")  # Пустая ячейка
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_widget.setItem(row_count, column, item)

    def save_data(self):
        data = []
        for row in range(self.table_widget.rowCount()):
            row_data = []
            for column in range(self.table_widget.columnCount()):
                if column >= 3:  # Для столбцов дней недели
                    combo = self.table_widget.cellWidget(row, column)  # Получение QComboBox
                    row_data.append(combo.currentText())  # Получение выбранного значения
                else:
                    item = self.table_widget.item(row, column)
                    row_data.append(item.text() if item else "")
            data.append(row_data)

        df = pd.DataFrame(data, columns=["Фамилия", "Имя", "Отчество", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница"])
        df.to_excel("veterinarian_schedule.xlsx", index=False)  # Сохранение данных в Excel
        QMessageBox.information(self, "Данные", "Изменения сохранены в veterinarian_schedule.xlsx")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableEditor()
    window.show()
    sys.exit(app.exec())

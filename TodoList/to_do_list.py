"""Задача 1: Простая база данных на JSON
 Напиши программу для управления списком задач (To-Do List). Данные хранятся в tasks.json.
        Программа должна иметь меню:
       Create - Добавить новую задачу (название, статус «не выполнено»).
       Read - Показать все задачи.
       Update - Отметить задачу как выполненную (по номеру или названию).
       Delete - Удалить задачу.
    После каждого действия обновленный список задач должен сохраняться в файл.
"""

import os 
import sys 
import json 
import uuid
from datetime import datetime 
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QMessageBox,
    QLabel, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon

"""Логика приложения"""

class ToDoList():
    def __init__(self, filename: str = "files/todolist.json"):
        self.filename = filename
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        self.notes = self.json_load()        
        
    def save(self):
        """Метод сохраняет заметку в json-файл"""        
        # Перезаписываем файл
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.notes, file, ensure_ascii=False, indent=4)
            
        print(f"Заметка {self.note} сохранена. Количество заметок: {len(self.notes)}")
                    
    def json_load(self):
        """Метод читает файл и загружает заметки в список"""
        notes = []
        if not os.path.exists(self.filename):            
            print(f"Файл с именем {self.filename} не найден!")
            return []
        if os.path.getsize(self.filename) == 0:
            print("Файл не содержит записей")  
            return [] 
        try:
            with open(self.filename, "r", encoding="utf-8") as file:                        
                notes = json.load(file)
                return notes                      
        except OSError:
            print("Ошибка чтения файла") 
            return [] 
    
    @staticmethod    
    def get_month(month: int) -> str:
        """Метод преобразует номер месяца в строчную запись"""
        months = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", 
                "Июля", "Августа", "Сентября", "Октября", "Ноября", "Декабря"]
        return months[month - 1]
        
    @staticmethod
    def get_day_of_week(day: int) -> str:
        """Метод возвращает строковое название дня недели"""
        days = ["Понедельник", "Вторник", "Среда", 
           "Четверг", "Пятница", "Суббота", "Воскресенье"]
        return days[day]    
       
    def get_date_time(self):
        """Метод возвращает строку с текущим
        днем недели, датой и временем"""
        date = str(datetime.now().day) + " " + str(self.get_month(datetime.now().month)) + " " + str(datetime.now().year)
        time = str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second)
        weekday = str(self.get_day_of_week(datetime.now().weekday()))
        return f"{weekday} {date} : {time}"
    
class NotePreprocessor(ToDoList):
    """Класс наследуется от ToDoList
    Управляет созданием и изменением заметок"""
    def __init__(self):
        super().__init__()
        self.done = False
        self.time = self.get_date_time()
        self.note_text = ""
        self.note = {}    
        
    def create(self, note_text: str):
        """Метод создает заметку в виде словаря"""
        if not note_text.strip():
            print("Заметка пустая")
            return
        new_note = {
            "id": str(uuid.uuid4()),
            "Название": note_text.strip(),
            "Статус": False,
            "Время": self.get_date_time()
            }
        self.notes.append(new_note)  # ← Добавляем в список
        self.note = new_note   
                                
    def update(self, number: int):
        """Заменяет статус задачи на True"""        
        if not self.notes:
            print("Нет сохранённых заметок")
            return None        
        note = self.find_note(number, self.notes)  
        if note and not note["Статус"]:
            note["Статус"] = True 
            # print("Статус заметки изменен")
            self.save()
            return 0 
        
    def read(self):
        """Метод печатает список задач"""
        notes = self.json_load()
        # if not notes:
        #     # print("Нет сохраненных заметок")        
        # for index, note in enumerate(notes):
        #     print("="*20, f"Заметка № {index + 1}", "="*40)
        #     for key, value in note.items():
        #         if key != "id":
        #             print(f"{key}: {value}")
        #     print("="*73)
            
    def find_note(self, number: int, notes: list):
        "Метод ищет заметку по номеру"
        try:
            assert type(number) is int
        except AssertionError:
            print("Введите целое число")
            return None      
        if 1 <= number <= len(notes):
            return notes[number - 1]
        else:
            print("Заметка с таким номером не найдена")
            return None
        
    def delete(self, number: int):
        """Удаляет заметку по номеру"""
        if not isinstance(number, int):
            print("Номер заметки должен быть целым числом.")
            return
        if 1 <= number <= len(self.notes):
            removed_note = self.notes.pop(number - 1)
            self.save()
            print(f"Заметка '{removed_note['Название']}' удалена.")
        else:
            print(f"Заметка с номером {number} не найдена.")
        
"""Графический интерфейс"""
            
class ToDoApp(QMainWindow):
    """Главное окно приложения. 
    Наследуется от QMainWindow""" 
    def __init__(self):
        super().__init__()
        self.todo = NotePreprocessor()
        self.init_ui()
        self.load_notes() 
        
    def init_ui(self):
        """Создает и настраивает интерфейс""" 
        # Настройка окна
        self.setWindowTitle(f"Аннигилятор срочных дел")
        self.setWindowIcon(QIcon("icon/icon.png"))
        self.resize(600, 500)
        
        # Стили
        self.setStyleSheet("""
            QMainWindow { 
            background-color: #35C0CD;
            font-size: 14px;
            }           
            QPushButton {
                background-color: #028E9B;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #015C65; }
            QPushButton:disabled { background-color: #5EC4CD; }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }                      
            QHeaderView::section {
                font-size: 14px;
                font-weight: bold;
                color: #333;
                background-color: #5EC4CD;
                padding: 6px;
                border: 1px solid #ccc;
            }
            QTableWidget {
                font-size: 12px;                
                color: #333;
            }
        """)
    
        # Главный виджет и вертикальный лэйаут
        main = QWidget()
        self.setCentralWidget(main)
        VLayout = QVBoxLayout(main)
        
        # Заголовок
        title = QLabel("Мой список выжившего")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Lucida Sans Unicode", 18, QFont.Bold))
        VLayout.addWidget(title)
        
        # Поле ввода + добавить
        input_layout = QHBoxLayout()
        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Не стесняйтесь, вываливайте сюда свои дела! 🗑️")
        self.add_btn = QPushButton("➕ Добавить и забыть")
        self.add_btn.clicked.connect(self.add_note) # Подписка на кнопку
        input_layout.addWidget(self.note_input)
        input_layout.addWidget(self.add_btn)        
        VLayout.addLayout(input_layout)
        
        # Виджет заметок
        self.note_table = QTableWidget()
        self.note_table.setColumnCount(3)
        self.note_table.setHorizontalHeaderLabels(["Список дел выжившего",
                                                   "Статус выживания",
                                                   "Точка отсчёта"])        
        self.note_table.setSelectionBehavior(self.note_table.SelectRows)
        self.note_table.setEditTriggers(self.note_table.NoEditTriggers) # Запрет редактирования
        header = self.note_table.horizontalHeader()
        header.setSectionResizeMode(2, header.Stretch)  
        VLayout.addWidget(self.note_table)
        
        # Кнопки интерфейса
        btn_layout = QHBoxLayout()
        self.done_btn = QPushButton("✅ Миссия выполнена")
        self.delete_btn = QPushButton("🗑 Аннигилировать")
        self.done_btn.clicked.connect(self.mark_done)
        self.delete_btn.clicked.connect(self.remove_note)
        btn_layout.addWidget(self.done_btn)
        btn_layout.addWidget(self.delete_btn)
        VLayout.addLayout(btn_layout)

        self.update_button_states()
        self.note_table.itemSelectionChanged.connect(self.update_button_states)

    def update_button_states(self):
        selected = bool(self.note_table.selectedItems())
        self.done_btn.setEnabled(selected)
        self.delete_btn.setEnabled(selected)

    def load_notes(self):
        """Загружает заметки в QTableWidget"""
        self.note_table.setRowCount(0) # Очищаем строки без заголовков        
        for note in self.todo.notes:
            row = self.note_table.rowCount()
            self.note_table.insertRow(row)
        
            title_note = QTableWidgetItem(note.get("Название", ""))
            status = "✅ Выполнено" if note.get("Статус") else "⏳ В процессе"
            status_note = QTableWidgetItem(status)
            status_note.setTextAlignment(Qt.AlignCenter)
            date_note = QTableWidgetItem(note.get("Время", ""))
            
            self.note_table.setItem(row, 0, title_note)
            self.note_table.setItem(row, 1, status_note)
            self.note_table.setItem(row, 2, date_note)
            
    def add_note(self):
        """Добавляет заметку в список задач"""
        text = self.note_input.text().strip()
        if not text:
            QMessageBox.warning(self, "Ошибка!", "Введите заметку!")
            return 
        self.todo.create(text)
        self.todo.save()
        self.note_input.clear()
        self.load_notes()
        
    def get_selected_row(self):
        """Возвращает выбранную заметку"""
        selected = self.note_table.selectionModel().selectedRows()
        return selected[0].row() if selected else None
    
    def mark_done(self):
        """Отмечает задачу как выполненную,
        перезаписывает файл"""      
        row = self.get_selected_row()
        if row is not None:
            self.todo.update(row + 1)  # потому что update ожидает номер с 1
            self.load_notes()    
 
    def remove_note(self):
        """Удаляет заметку и перезаписывает файл"""
        row = self.get_selected_row()
        if row is None:
            return
        notes = self.todo.json_load()
        if 0 <= row < __builtins__.len(self.todo.notes):
            removed = self.todo.notes.pop(row)
            self.todo.save()
            QMessageBox.information(self, "Аннигилировано!", f"Задача '{removed['Название']}' удалена.")
            self.load_notes() 
        else:
            QMessageBox.warning(self, "Ошибка", "Задача не найдена.")        
        

"""Запуск приложения"""
 
if __name__ == "__main__":
    app = QApplication(sys.argv)     
    window = ToDoApp()             
    window.show()                     
    sys.exit(app.exec_())             
                    



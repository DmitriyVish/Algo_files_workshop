"""Конвертер форматов (TXT -> JSON)
В файле users.txt данные хранятся в формате:
    Имя:Алексей,Возраст:30,Город:Москва
    Напиши программу, которая читает этот файл, парсит каждую строку и сохраняет результат в файл users.json в виде списка словарей:
    [{"Имя": "Алексей", "Возраст": "30", "Город": "Москва"}, ...]
"""
import os
import json

FILENAME = "users.txt"

def file_reader(filename: str):
    """Функция для чтения файла"""
    try:
        if os.path.exists(filename):        
            try:
                if os.path.getsize(filename) != 0:
                    with open(filename, "r", encoding="utf-8") as file:
                        lines = [line for line in file] 
                        return lines                           
                else:
                    print("В файле нет записей")
            except IOError:
                print("Файл не может быть прочитан")
    except FileNotFoundError:
        print("Файл не найден")

def string_parser(line: str) -> list:
    """Функция разбивает строку по двоеточию
    и возвращает скисок из двух строк"""
    try:
        assert type(line) is str
    except AssertionError:
        print("Тип данных должен быть - строка")
        return 1
    if ":" not in line:
        print("Неверный формат токена")
        return 2
    else:
        is_colon = False      
        key, value = "", ""
        for elem in line:    
            if elem == ":":
                is_colon = True
            elif not is_colon:
                key += elem 
            else:
                value += elem
        return [key, value]

def string_preprocessor():
    users_list = []    
    tokens = file_reader(FILENAME)
    if tokens:
        for token in tokens:
            user_dict = {}
            rows = token.replace("\n", "")
            rows = rows.split(",")
            for token in rows:
                key, value = string_parser(token) 
                user_dict[key] = value   
            users_list.append(user_dict)
    else:
        print("Нет данных для преобразования")  
    return users_list  

def save_to_json(filename: str):
    """Функция записывает данные в файл формата json"""
    data = string_preprocessor()
    if not data:
            print("Нет данных для сохранения в JSON")
            return 1 
    else:
        if not os.path.exists(filename):        
            with open(filename, 'w+', encoding='utf-8') as file:
                try:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                    print(f"Данные успешно сохранены в файл {filename}")
                except IOError as e:
                    print(f"Ошибка при сохранении файла: {str(e)}")
        else:
            return 1
   

try:
    save_to_json("users.json")
except Exception as e:
    print(f"Произошла ошибка при сохранении: {str(e)}")
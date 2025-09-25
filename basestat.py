"""Задача 2: Чтение списка и базовая статистика (TXT)
В файле numbers.txt хранятся числа, каждое на новой строке. 
Напиши программу, которая прочитает файл, выведет все числа на экран и посчитает
их сумму, среднее арифметическое, максимальное и минимальное значение.
"""
import os 
import numpy as np  

def number_generator(start: int, stop: int, count: int) -> list:
    """Функция случайно генерирует последовательность целых чисел"""
    try:
        assert type(start) is int and type(stop) is int and type(count) is int
        assert 0 < count <= 1e6
        return list(np.random.randint(1, 1000000, count))
    except AssertionError:
        return 1
    
def write_note(mode: str="w+"):
    """Функция для записи в текстовый файл"""
    with open("files/numbers.txt", mode=mode, encoding="utf-8") as file: 
        numbers = number_generator(132, 97658, 100)   
        if not numbers:
            print("В списке нет записей")
        else:
            for number in numbers:             
                try:
                    file.write(f"{str(number)}\n") 
                    print("Запись успешно добавлена!")                    
                except IOError as e:
                    print(f"Ошибка при записи в файл: {e}")
"""
# Считывание и запись в файл
if not os.path.exists("files/numbers.txt"):
    write_note() 
else:
    write_note("a")
"""

#  Чтение файла для проверки
if not os.path.exists("files/numbers.txt"):
    print("Файла не существует!")
else:
    with open("files/numbers.txt", "r", encoding="utf-8") as file:
        try:
            elements = [float(line) for line in file]
        except TypeError: 
            print("Неверные данные!")  
                     
print(f"Данные из файла 'numbers.txt': {elements} \n")
print(f"Сумма: {np.sum(elements)} \n")
print(f"Среднее арифметическое: {np.mean(elements)} \n")
print(f"Максимальное значение: {np.max(elements)} \n")
print(f"Минимальное значение: {np.min(elements)}")
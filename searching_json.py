"""
Задача 2: Поиск и фильтрация в данных (JSON)
Программа загружает из файла products.json список товаров (каждый товар - словарь с полями name, price, category). Предложи пользователю:
1.  Вывести все товары из категории «еда». = Продукты
2.  Вывести товары дороже 100 рублей.
3.  Найти товар по названию.
"""

import json 
import numpy as np  
import pandas as pd  

print("-"*20, "Строки из датасета", "-"*80)
data = pd.read_json("files/products.json")
print(data.sample(10))
print("-"*100, end="\n")

print("-"*20,'Товары из категории "Продукты"',"-"*48)
products_list = data[data["category"] == "Продукты"]["name"].to_list()
print(*products_list, sep="\n")
print("-"*100, end="\n")

print("-"*20,"Товары дороже 100 рублей","-"*54)
print(data[data["price"] > 100].sort_values(by="category").reset_index(drop=True))
print("-"*100, end="\n")

print("-"*20,"Найти товар по названию","-"*55)
print("*"*20,"Товары в наличии","*"*55)
print(data["name"].unique())
print("*"*100)
print(data[data["name"] == input("Введите название товара из списка: ")])
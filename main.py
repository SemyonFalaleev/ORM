import sqlalchemy as sq
import json
from sqlalchemy.orm import sessionmaker
from models import  DataBase, Publisher, Sale, Shop, Stock, Book

if __name__ == "__main__":
# Создаём объект класса DataBase, этот объект отвечает
# за соединение с базой данных 
    test = DataBase("login", "password", "name_db")

# Создаём таблицы в базе данных 
    test.create_tables()

# Загружаем информацию в базу данных из json файла
    test.load_json_db("path_to_json_file")

# Функция производит запрос выборки магазинов, продающих целевого издателя.
    test.searching_author()


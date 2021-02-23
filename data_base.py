from pymongo import MongoClient

connection = "mongodb+srv://velllum:0sxfeDlou9i66twP@cluster0.fs8kg.mongodb.net/freelancers?retryWrites=true&w=majority"

client = MongoClient(connection)
db = client.freelancers["stomshop_pro"]


def save_data(dic):
    """- Сохраняет собранные данные в удаленную базу mongodb"""
    try:
        db.insert(dic)
    except Exception as e:
        print(f"Произошла ошибка {e}")


def remove_data():
    """- Отчистить базу от всех данных"""
    db.delete_many({})

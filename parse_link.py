import requests
from pymongo import MongoClient


connection = "mongodb+srv://velllum:0sxfeDlou9i66twP@cluster0.fs8kg.mongodb.net/freelancers?retryWrites=true&w=majority"

client = MongoClient(connection)
db = client.freelancers["stomshop_pro"]

base_dict = dict(

    category=None,
    subcategory=None,
    subsubcategory=None,

    link=None,
    code_and_article=None,
    product_name=None,
    presence_in_stock=None, # Наличие: На складе
    will_deliver=None, # Доставим по Санкт-Петербургу уже на следующий день.
    brand=None, # Бренд: Vatech (Ю. Корея)

# 1) (Код товара: S-11282) - без скобочек бывает так в этом поле S-7807, Артикул: 492-9000====
# 2) наименование товара====
# 3) Сылка====
# 4) категории====
# 5) подкатегории ( до 5-6 вроде встречал)====
# 6) Наличие: На складе====
# 7) Доставим по Санкт-Петербургу уже на следующий день.====
# 8) Бренд: Vatech (Ю. Корея)===
# 9) Подходит для лицензирования
# 10) Бесплатная доставка!
# 11)цена 194 870 р.
# 12) зачеркнутая цена 233 250 р.
# 13) наличие такого текста  Получите дополнительную скидку
# 14) Гарантия если указана-  Гарантия, месяцев: 24 (рентген), 6 (аккумулятор)
# 15) файлы по ссылкам из описания - Брошюра EzRay Air Portable на русском языке (скачать)
# Руководство по эксплуатации EzRay Air Portable на русском языке (скачать)
# 16) технические характеристики
# 17) отзывы,
# 18) вопрос ответы
# 19) регистрационные документы
# 20) Стикеры от товара  - Новинка, Бесплатная доставка, Акция до 28.02.2021
# 21) описание



headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"}


def _get_respose(self):
    """
    - Получить ответ запросы по ссылке

    :return: None
    """
    with requests.Session() as session:
        session.headers = self._headers

        response = session.get(url=)
        if response.ok:
            self._response = response
        else:
            print('ОШИБКА - 404')



def _save_data(self):
    """
    - Сохраняет собранные данные в удаленную базу mongodb

    :return: None
    """
    try:
        self.db.insert_many(self.list_items["result"]["items"])
    except Exception as e:
        print(f"Произошла ошибка {e}")



def remove_data(self):
    """
    - Отчистить базу от всех данных

    :return: None
    """
    self.db.delete_many({})



def run(self):
    """
    - Метод старта программ

    :return: None
    """
    while True:
        self._get_respose()
        self.list_items = self._response.json()

        if not self.list_items["result"]["items"]:
            print(f"Загрузка закончена, собранное количество {self.db.count_documents({})}")
            break

        self._save_data()
        ParseArshin._PAGE_NUMBER += 1


def __str__(self):
    return print(f"{self.list_items} | {self.list_items*1000}")


if __name__ == '__main__':
    parse = ParseArshin()
    # parse.remove_data()
    # parse.run()

    for e, field in enumerate(parse.db.find({"properties.value": "37049-08"}, {"_id": 0}), 1):
        # print(e, field["properties"][1]["value"],   field["properties"][10]["value"][0], field["properties"][4]["value"])
        print(e, )
import csv
import os
from pathlib import Path

import requests
from selenium import webdriver
import time

from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys

from dict_base import base_dic

import data_base

user_agent = UserAgent()

base_path = os.path.abspath(os.path.dirname(__file__))
path_registration_documents = os.path.join(base_path, "files", "registration_documents")
path_files_description = os.path.join(base_path, "files", "files_description")

# options
options = webdriver.ChromeOptions()

options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless")
options.add_experimental_option('prefs', {
    "download.default_directory": path_registration_documents,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True,
}
                                )

driver = webdriver.Chrome(
    executable_path=f"{base_path}/chromedriver",
    options=options
)


def author():
    """Авторизация на сайте"""
    driver.get("https://stomshop.pro/login/")
    time.sleep(1)

    email_input = driver.find_element_by_id("input-email")
    email_input.clear()
    email_input.send_keys("velllum@ya.ru")
    time.sleep(1)

    password_input = driver.find_element_by_id("input-password")
    password_input.clear()
    password_input.send_keys("123456789")
    time.sleep(1)

    password_input.send_keys(Keys.ENTER)

    time.sleep(1)

    print("Авторизация прошла успешно")


def downloads_done():
    for i in os.listdir(path_registration_documents):
        if ".crdownload" in i:
            time.sleep(0.5)
            downloads_done()


def save_files():
    """ - Сохраняет файлы"""

    driver.find_element_by_id("tab-documentation-li").click()
    time.sleep(0.5)

    documents = driver.find_elements_by_class_name("docext-container")

    for document in documents:
        document.click()
        time.sleep(1)
    downloads_done()

    print(f"РЕГИСТРАЦИООНЫЕ ДОКУМЕНТЫ БИЛИ СОХРАНЕНЫ В КОЛИЧЕСТВЕ {len(documents)}")

    return len(documents)


def get_name_file(number_files):
    """ - Получить имена файлов "Регистрационные документы"""
    file_list = os.listdir(path_registration_documents)
    full_list = [os.path.join(path_registration_documents, i) for i in file_list]
    time_sorted_list = sorted(full_list, key=os.path.getmtime, reverse=True)
    list_file_name = [name.split("/")[-1] for name in time_sorted_list[:number_files]]
    files_name = " | ".join(list_file_name)
    return files_name


def get_list_all_links_product():
    """Получить список всех ссылок с товарами"""
    with open('links_product.csv', "r") as f:
        reader = csv.reader(f)
        data = list(reader)
    data = [d[0] for d in data]

    print("Данные из файла были собраны")

    return data


def get_category():
    """Получить весь путь категорий, строку пути до продукта"""
    breadcrumb = driver.find_element_by_xpath("//ul[@class='breadcrumb text-center']")
    list_category = breadcrumb.find_elements_by_tag_name('li')
    list_category = [category.text for category in list_category]
    category = " | ".join(list_category)
    return category


def get_product_name():
    """Получить заголовок h1"""
    title = driver.find_element_by_xpath("//div[@class='h2 text-center content-title']")
    tag_h1 = title.find_element_by_tag_name('h1')
    return tag_h1.text


def get_code_and_article():
    """Получить артикул товара и код товара"""
    title = driver.find_element_by_xpath("//div[@class='h2 text-center content-title']")
    code_and_article = title.find_element_by_xpath("//div[@class='h2']")
    code_and_article = str(code_and_article.text).replace("(", "").replace(")", "")
    return code_and_article


def get_presence_in_stock():
    """Получить подтверждение о наличии товара на складе"""
    presence = driver.find_element_by_xpath("//p[@class='h4-product']")
    return presence.text


def get_will_deliver():
    """Получить строку Доставим по Санкт-Петербургу уже на следующий день"""
    presence = driver.find_element_by_xpath("//div[@class='stock-7']")
    deliver = presence.find_element_by_xpath("//span[@class='prmn-cmngr-message']")
    return str(deliver.text).split(".")[0]


def get_brand():
    """Получить бренд товара"""
    brand = driver.find_elements_by_xpath("//div[@class='stock-7']")[1]
    name_brand = brand.find_element_by_tag_name("h4")
    return name_brand.text


def get_license():
    """Получить сообщение об лицензии"""
    message = driver.find_elements_by_xpath("//div[@class='stock-7']")[2]
    license_message = message.find_element_by_tag_name("h4")
    return license_message.text


def get_free_delivery():
    """Получить сообщение о бесплатной доставке"""
    free_delivery = driver.find_elements_by_xpath("//h4[@class='text-special']")[1]
    return free_delivery.text


def get_price():
    """Получить новую цену товара"""
    price = driver.find_element_by_xpath("//span[@class='price-1-new']")
    return price.text


def get_strikethrough_price():
    """Получить старую цену товара"""
    strikethrough_price = driver.find_element_by_xpath("//span[@class='price-old']")
    return strikethrough_price.text


def get_discount():
    """Получить сообщение о дополнительной скидке"""
    discount = driver.find_element_by_xpath("//a[@class='link-cheaper']")
    return discount.text


def get_warranty():
    """Получить сообщение о гарантии ..."""
    warranty = driver.find_element_by_xpath("//div[@id='product-warranty-block']")
    return warranty.text


def get_technical_specifications():
    """Получить технические характеристики товара"""
    text_list = []
    table_responsive = driver.find_elements_by_class_name("table")[0]
    for tr in table_responsive.find_elements_by_tag_name("tr"):
        table_data = [td.get_attribute("innerHTML") for td in
                      tr.find_elements_by_tag_name("td") or tr.find_elements_by_tag_name("strong")]
        text_list.append(" | ".join(table_data))
    table_text = "\n".join(text_list)
    return table_text


def get_stickers():
    """Получить все стикеры товара"""
    stickers = driver.find_element_by_xpath("//div[@class='xd_stickers_wrapper xd_stickers_product']")
    stickers_list = stickers.find_elements_by_class_name("xd_stickers")
    return " | ".join([sticker.text for sticker in stickers_list])


def get_product_description():
    """Получить описание товара"""
    product_description = driver.find_elements_by_id("tab-description")
    list_product_description = []

    for product in product_description:
        list_product_description.append(product.text)

    list_product_description = list_product_description[0].split("\n")
    list_product_description = [str(text).strip() for text in list_product_description]
    return "\n".join(list_product_description)


def get_reviews():
    """Получить отзывы о товаре"""
    reviews = driver.find_element_by_id("review")
    div = reviews.find_elements_by_tag_name("p")
    list_tsxt = []
    for i in div:
        list_tsxt.append(i.get_attribute("innerHTML"))
    table_text = "\n".join(list_tsxt)
    return table_text


def get_name_files_description_and_save_files():
    """Получить имена  файлов описания товара и сохранить их  в папку"""
    links_file = driver.find_elements_by_xpath("//a[@style='text-decoration:none;']")
    links = [link.get_attribute("href") for link in links_file]
    list_file_name = []

    for url in links:
        file_name = str(url).split("/")[-1]
        list_file_name.append(file_name)

        path_file = os.path.join(path_files_description, file_name)

        filename = Path(path_file)
        response = requests.get(url)
        filename.write_bytes(response.content)

    text_name = " | ".join(list_file_name)
    return text_name


def main():
    try:

        count = 0

        # data_base.remove_data()  # отчищаем базу данных

        # time.sleep(2)

        list_links_product = get_list_all_links_product()  # получаем список из csv файла

        author()  # запускаем авторизацию на сайте

        for e, link in enumerate(list_links_product, 1):

            print(e, link)
            print("_" * 100)

            driver.get(link)

            try:
                """Получить описание товара"""
                base_dic["description"] = get_product_description()
            except:
                base_dic["description"] = "Отсутствует"
                print(f'description = "Отсутствует"')

            try:
                """Добавляем ссылку товара в словарь"""
                base_dic["link_product"] = link
            except:
                base_dic["link_product"] = "Отсутствует"
                print(f'link_product = "Отсутствует"')

            try:
                """Добавляем путь категории до товара в словарь"""
                base_dic["category"] = get_category()
            except:
                base_dic["category"] = "Отсутствует"
                print(f'category= "Отсутствует"')

            try:
                """Получить заголовок h1"""
                base_dic["product_name"] = get_product_name()
            except:
                base_dic["product_name"] = "Отсутствует"
                print(f'product_name = "Отсутствует"')

            try:
                """Получить артикул товара и код товара"""
                base_dic["code_and_article"] = get_code_and_article()
            except:
                base_dic["code_and_article"] = "Отсутствует"
                print(f'code_and_article = "Отсутствует"')

            try:
                """Получить подтверждение о наличии товара на складе"""
                base_dic["presence_in_stock"] = get_presence_in_stock()
            except:
                base_dic["presence_in_stock"] = "Отсутствует"
                print(f'presence_in_stock = "Отсутствует"')

            try:
                """Доставим по Санкт-Петербургу уже на следующий день"""
                base_dic["will_deliver"] = get_will_deliver()
            except:
                base_dic["will_deliver"] = "Отсутствует"
                print(f'will_deliver = "Отсутствует"')

            try:
                """Получить бренд товара"""
                base_dic["brand"] = get_brand()
            except:
                base_dic["brand"] = "Отсутствует"
                print(f'brand= "Отсутствует"')

            try:
                """Получить сообщение об лицензии"""
                base_dic["license"] = get_license()
            except:
                base_dic["license"] = "Отсутствует"
                print(f'license = "Отсутствует"')

            try:
                """Получить сообщение о бесплатной доставке"""
                base_dic["free_delivery"] = get_free_delivery()
            except:
                base_dic["free_delivery"] = "Отсутствует"
                print(f'free_delivery = "Отсутствует"')

            try:
                """Получить новую цену товара"""
                base_dic["price"] = get_price()
            except:
                base_dic["price"] = "Отсутствует"
                print(f'price = "Отсутствует"')

            try:
                """Получить старую цену товара"""
                base_dic["strikethrough_price"] = get_strikethrough_price()
            except:
                base_dic["strikethrough_price"] = "Отсутствует"
                print(f'strikethrough_price = "Отсутствует"')

            try:
                """Получить сообщение о дополнительной скидке"""
                base_dic["discount"] = get_discount()
            except:
                base_dic["discount"] = "Отсутствует"
                print(f'discount = "Отсутствует"')

            try:
                """Получить сообщение о гарантии ..."""
                base_dic["warranty"] = get_warranty()
            except:
                base_dic["warranty"] = "Отсутствует"
                print(f'warranty = "Отсутствует"')

            try:
                """Получить технические характеристики товара"""
                base_dic["technical_specifications"] = get_technical_specifications()
            except:
                base_dic["technical_specifications"] = "Отсутствует"
                print(f'technical_specifications = "Отсутствует"')

            try:
                """Получить имена файлов регистрационных документов"""
                number_files = save_files()  # Сохраняет файлы registration_documents
                base_dic["registration_documents"] = get_name_file(number_files)
            except:
                base_dic["registration_documents"] = "Отсутствует"
                print(f'registration_documents = "Отсутствует"')

            try:
                """Получить все стикеры товара"""
                base_dic["stickers"] = get_stickers()
            except:
                base_dic["stickers"] = "Отсутствует"
                print(f'stickers = "Отсутствует"')

            try:
                """Получить отзывы о товаре"""
                base_dic["reviews"] = get_reviews()
            except:
                base_dic["reviews"] = "Отсутствует"
                print(f'reviews = "Отсутствует"')

            try:
                """Получить имена  файлов описания товара и сохранить их  в папку"""
                base_dic["files_description"] = get_name_files_description_and_save_files()
            except:
                base_dic["files_description"] = "Отсутствует"
                print(f'files_description = "Отсутствует"')

            data_base.save_data(base_dic)

            count += 1

            print(count, base_dic)
            print("=" * 100)

            base_dic.clear()  # отчищаем словарь о данных

            # if count == 1:
            #     break

    except Exception as ex:
        print("ошибка", ex)

    finally:
        print("Окончание работы программы")
        driver.close()
        driver.quit()


if __name__ == '__main__':
    main()

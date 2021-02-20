import os
from telnetlib import EC

from selenium import webdriver
import time

from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

user_agent = UserAgent()
base_path = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(base_path, "files")

# options
options = webdriver.ChromeOptions()

options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--start-maximized")
options.add_argument("--headless")
options.add_experimental_option('prefs',  {
        "download.default_directory": file_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
        # "plugins.plugins_disabled": ["Chrome PDF Viewer"]

    }
)


driver = webdriver.Chrome(
    executable_path=f"{base_path}/chromedriver",
    options=options
)


def author():
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


try:
    author()
    driver.get("https://stomshop.pro/woodpecker-led-d")
    driver.find_element_by_id("tab-documentation-li").click()
    time.sleep(1)
    print(driver.find_element_by_tag_name('a').get_attribute('href'))  # "innerHTML"
    print(driver.find_element_by_class_name('documentation-download').get_attribute("innerHTML"))  # "innerHTML"
    driver.find_element_by_class_name("docext-container").click()
    time.sleep(1)
    # driver.find_element("text-decoration:none;").click()
    # driver.find_element_by_xpath("//i[@class='fa-download']").click()


    driver.find_element_by_xpath('//a[@style="text-decoration:none;"]').get_attribute('href')


except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

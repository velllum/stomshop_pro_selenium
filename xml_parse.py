import requests
from bs4 import BeautifulSoup

respose = requests.get("https://stomshop.pro/sitemap.xml")

xml = BeautifulSoup(respose.text, "xml")

print(len(xml.find_all("loc")))

for url in xml.find_all("loc"):
    print(url.text)

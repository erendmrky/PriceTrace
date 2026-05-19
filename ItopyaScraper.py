import urllib.parse
import requests
from bs4 import BeautifulSoup
from typing_extensions import override
from BaseScraper import BaseScraper
from ProductResult import ProductResult

class ItopyaScraper(BaseScraper):
    CATEGORIES = {
        "cpu" : "islemci-q8",
        "gpu" : "ekran-karti-q11",
        "ram" : "rambellek-q10",
        "motherboard": "anakart-q9",
        "ssd" : "ssd-q20",
        "psu" : "powersupply-q17"
    }
    def __init__(self,category_select,users_input):
        self.category_select = category_select
        self.users_input = users_input

    @override
    def scrape(self):
        search_url = self.build_search_url()
        response= requests.get(search_url, headers=self.headers)
        soup= BeautifulSoup(response.text, "html.parser")
        cart_items = soup.find_all("div", class_="product-block")
        for items in cart_items:
            title = items.find("a", class_="title").get_text()
            if self.users_input.lower() in title.lower():
                priceTag = items.find("strong")
                raw_price = priceTag.getText(strip=True)
                parsed_price = self._parse_price(raw_price)
                result = ProductResult("İtopya",title,parsed_price)
                return result
        return None

    @override
    def build_search_url(self):
        category_id = self.CATEGORIES.get(self.category_select.lower(),"")
        safe_query = urllib.parse.quote(self.users_input)
        url = f"https://www.itopya.com/ara?bul={safe_query}&kategori={category_id}"
        return url

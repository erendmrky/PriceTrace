import urllib.parse
import requests
import re
from bs4 import BeautifulSoup
from typing_extensions import override
from BaseScraper import BaseScraper
from ProductResult import ProductResult
from requests.exceptions import RequestException

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

        try:
            response = requests.get(search_url, headers=self.headers, timeout=10)
        except RequestException:
            return ProductResult("İtopya", "TIMEOUT", 0)

        if response.status_code != 200:
            return ProductResult("İtopya","BANNED",0)

        soup= BeautifulSoup(response.text, "html.parser")
        cart_items = soup.find_all("div", class_="product-block")

        search_terms = self.users_input.lower().split()

        for items in cart_items:
            title_tag = items.find("a", class_="title")
            if not title_tag:
                continue

            title = title_tag.getText(strip=True)

            if all(re.search(rf"\b{re.escape(term)}\b", title.lower()) for term in search_terms):
                price_tag = items.find("strong")
                if price_tag is not None:
                    raw_price = price_tag.getText(strip=True)
                    parsed_price = self._parse_price(raw_price)
                    return ProductResult("İtopya",title,parsed_price)

        return ProductResult("İtopya", "EMPTY", 0)

    @override
    def build_search_url(self):
        category_id = self.CATEGORIES.get(self.category_select.lower(),"")
        safe_query = urllib.parse.quote(self.users_input)
        url = f"https://www.itopya.com/ara?bul={safe_query}&kategori={category_id}&or=edf"
        return url

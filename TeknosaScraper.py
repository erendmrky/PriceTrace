import urllib.parse
import requests
import re
from bs4 import BeautifulSoup
from typing_extensions import override
from BaseScraper import BaseScraper
from ProductResult import ProductResult
from requests.exceptions import RequestException

class TeknosaScraper(BaseScraper):
    CATEGORIES = {
        "cpu" : "islemci-c-116001001",
        "gpu" : "ekran-karti-c-116001004",
        "ram" : "ram-c-116001003",
        "motherboard": "anakart-c-116001002",
        "ssd" : "ssd-c-116001008",
        "psu" : "guc-kaynagi-c-116001005"
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
            return ProductResult("Teknosa", "TIMEOUT", 0)

        if response.status_code != 200:
            return ProductResult("Teknosa","BANNED",0)

        soup= BeautifulSoup(response.text, "html.parser")
        cart_items = soup.find_all("ul", class_="prd  non-style")

        search_terms = self.users_input.lower().split()

        for items in cart_items:
            title_tag = items.find("h3", class_="prd-title prd-title-style")
            if not title_tag:
                continue

            title = title_tag.getText(strip=True)

            if all(re.search(rf"\b{re.escape(term)}\b", title.lower()) for term in search_terms):
                price_tag = items.find("span", class_="prc prc-last ")
                if price_tag is not None:
                    raw_price = price_tag.getText(strip=True)
                    parsed_price = self._parse_price(raw_price)
                    return ProductResult("Teknosa",title,parsed_price)

        return ProductResult("Teknosa", "EMPTY", 0)

    @override
    def build_search_url(self):
        category_id = self.CATEGORIES.get(self.category_select.lower(),"")
        safe_query = urllib.parse.quote(self.users_input)
        url = f"https://www.teknosa.com/{category_id}/?s={safe_query}%3Aprice-desc"
        return url
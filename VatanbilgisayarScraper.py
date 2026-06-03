import urllib.parse
import requests
import re
from bs4 import BeautifulSoup
from typing_extensions import override
from BaseScraper import BaseScraper
from ProductResult import ProductResult
from requests.exceptions import RequestException

class VatanbilgisayarScraper(BaseScraper):
    CATEGORIES = {
        "cpu" : "islemciler",
        "gpu" : "ekran-kartlari",
        "ram" : "bilgisayar-ram-bellek",
        "motherboard": "anakart",
        "ssd" : "solid-state-disk",
        "psu" : "guc-kaynaklari-power"
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
            return ProductResult("Vatanbilgisayar", "TIMEOUT", 0)

        if response.status_code != 200:
            return ProductResult("Vatanbilgisayar","BANNED",0)

        soup= BeautifulSoup(response.text, "html.parser")
        cart_items = soup.find_all("a", class_="product-list-link")

        search_terms = self.users_input.lower().split()

        for items in cart_items:
            title_tag = items.find("div",class_="product-list__product-name")
            if not title_tag:
                continue

            title = title_tag.getText(strip=True)

            if all(re.search(rf"\b{re.escape(term)}\b", title.lower()) for term in search_terms):
                price_tag = items.find("span",class_="product-list__price")
                if price_tag is not None:
                    raw_price = price_tag.getText(strip=True)
                    parsed_price = self._parse_price(raw_price)
                    return ProductResult("Vatanbilgisayar",title,parsed_price)

        return ProductResult("Vatanbilgisayar", "EMPTY", 0)


    @override
    def build_search_url(self):
        category_id = self.CATEGORIES.get(self.category_select.lower(),"")
        safe_query = urllib.parse.quote(self.users_input)
        url = f"https://www.vatanbilgisayar.com/arama/{safe_query}/{category_id}/?srt=UP"
        return url


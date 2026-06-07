import urllib.parse
import requests
import re
from bs4 import BeautifulSoup
from typing_extensions import override
from BaseScraper import BaseScraper
from ProductResult import ProductResult
from requests.exceptions import RequestException


class IncehesapScraper(BaseScraper):
    CATEGORIES = {
        "cpu": "islemci",
        "gpu": "ekran-karti",
        "ram": "ram-bellek",
        "motherboard": "anakart",
        "ssd": "ssd-harddisk",
        "psu": "power-supply"
    }

    def __init__(self, category_select, users_input):
        self.category_select = category_select
        self.users_input = users_input

    @override
    def scrape(self):
        search_url = self.build_search_url()

        try:
            response = requests.get(search_url, headers=self.headers, timeout=10)
        except RequestException:
            return ProductResult("İncehesap", "TIMEOUT", 0)

        if response.status_code != 200:
            return ProductResult("İncehesap", "BANNED", 0)

        soup = BeautifulSoup(response.text, "html.parser")
        search_terms = self.users_input.lower().split()

        all_items = soup.find_all("a", class_=lambda c: c and "product" in c)

        for item in all_items:

            title_tag = item.find("div", {"itemprop": "name"})
            if not title_tag:
                continue

            title = title_tag.getText(strip=True)

            if all(re.search(rf"\b{re.escape(term)}\b", title.lower()) for term in search_terms):

                price_tag = item.find("span", {"itemprop": "price"})
                rel_url = item.get("href")
                link = "https://www.incehesap.com/"+str(rel_url)

                if price_tag is not None:
                    raw_price = price_tag.getText(strip=True)
                    parsed_price = self._parse_price(raw_price)

                    return ProductResult("İncehesap", title, parsed_price,link)

        return ProductResult("İncehesap", "EMPTY", 0)

    @override
    def build_search_url(self):
        category_id = self.CATEGORIES.get(self.category_select.lower(), "")
        safe_query = urllib.parse.quote(self.users_input)

        url = f"https://www.incehesap.com/q/{safe_query}/{category_id}"

        return url
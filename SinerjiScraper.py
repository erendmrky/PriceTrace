import urllib.parse
import requests
import re
from bs4 import BeautifulSoup
from typing_extensions import override
from BaseScraper import BaseScraper
from ProductResult import ProductResult
from requests.exceptions import RequestException


class SinerjiScraper(BaseScraper):
    CATEGORIES = {
        "cpu": "islemci",
        "gpu": "ekran-karti",
        "ram": "bellek-ram",
        "motherboard": "anakart",
        "ssd": "depolama",
        "psu": "guc-kaynagi"
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
            return ProductResult("Sinerji", "TIMEOUT", 0)

        if response.status_code != 200:
            return ProductResult("Sinerji", "BANNED", 0)

        soup = BeautifulSoup(response.text, "html.parser")
        search_terms = self.users_input.lower().split()

        all_items = soup.find_all("article", class_=lambda c: c and "product" in c)

        for item in all_items:

            title_div = item.find("div", class_="title")
            if not title_div:
                continue

            title_tag = title_div.find("a")
            if not title_tag:
                continue

            title = title_tag.getText(strip=True)

            if all(re.search(rf"\b{re.escape(term)}\b", title.lower()) for term in search_terms):
                rel_url = title_tag.get("href")
                link = "https://www.sinerji.gen.tr/"+rel_url
                price_tag = item.find("span", class_="price")

                if price_tag is not None:
                    raw_price = price_tag.getText(strip=True)
                    parsed_price = self._parse_price(raw_price)

                    return ProductResult("Sinerji", title, parsed_price,link)

        return ProductResult("Sinerji", "EMPTY", 0)

    @override
    def build_search_url(self):
        category_id = self.CATEGORIES.get(self.category_select.lower(), "")
        safe_query = self.users_input.strip().lower().replace(" ", "-")

        url = f"https://www.sinerji.gen.tr/{safe_query}-s-{category_id}"

        return url
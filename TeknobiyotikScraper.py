import urllib.parse
import re
from bs4 import BeautifulSoup
from typing_extensions import override
from BaseScraper import BaseScraper
from ProductResult import ProductResult
from requests.exceptions import RequestException
import requests


class TeknobiyotikScraper(BaseScraper):
    CATEGORIES = {
        "cpu": "33",
        "gpu": "217",
        "ram": "31",
        "motherboard": "62",
        "ssd": "175",
        "psu": "61"
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
            return ProductResult("Teknobiyotik", "TIMEOUT", 0)

        if response.status_code != 200:
            return ProductResult("Teknobiyotik", "BANNED", 0)

        soup = BeautifulSoup(response.text, "html.parser")
        search_terms = self.users_input.lower().split()

        all_h3 = soup.find_all("h3")

        for h3_tag in all_h3:
            a_tag = h3_tag.find("a")
            if not a_tag:
                continue

            title = a_tag.get("title", "").strip() or a_tag.getText(strip=True)

            if all(re.search(rf"\b{re.escape(term)}\b", title.lower()) for term in search_terms):

                link = str(a_tag.get("href"))
                price_box = h3_tag.find_next("div", class_="price-box")

                if price_box:
                    price_tag = price_box.find("span", class_="price")

                    if price_tag is not None:
                        raw_price = price_tag.getText(strip=True)
                        parsed_price = self._parse_price(raw_price)

                        return ProductResult("Teknobiyotik", title, parsed_price,link)

        return ProductResult("Teknobiyotik", "EMPTY", 0)

    @override
    def build_search_url(self):
        category_id = self.CATEGORIES.get(self.category_select.lower(), "")
        safe_query = urllib.parse.quote(self.users_input)

        url = f"https://www.teknobiyotik.com/catalogsearch/result/index/?cat={category_id}&q={safe_query}"

        return url

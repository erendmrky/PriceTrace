import urllib.parse
import requests
import re
from bs4 import BeautifulSoup
from typing_extensions import override
from BaseScraper import BaseScraper
from ProductResult import ProductResult
from requests.exceptions import RequestException


class MediaMarktScraper(BaseScraper):
    CATEGORIES = {
        "cpu" : "CAT_TR_MM_504925//CAT_TR_MM_641508//CAT_TR_MM_679036",
        "gpu" : "CAT_TR_MM_504925//CAT_TR_MM_641508//CAT_TR_MM_679035",
        "ram" : "CAT_TR_MM_504925//CAT_TR_MM_641508//CAT_TR_MM_798060",
        "motherboard": "CAT_TR_MM_504925//CAT_TR_MM_641508//CAT_TR_MM_798063",
        "ssd" : "CAT_TR_MM_504925//CAT_TR_MM_641508//CAT_TR_MM_798099",
        "psu" : "CAT_TR_MM_504925//CAT_TR_MM_641508//CAT_TR_MM_797541"
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
            return ProductResult("MediaMarkt", "TIMEOUT", 0)

        if response.status_code != 200:
            return ProductResult("MediaMarkt","BANNED",0)


        soup = BeautifulSoup(response.text, "html.parser")
        search_terms = self.users_input.lower().split()
        all_items = soup.find_all("article", {"data-test": "mms-product-card"})

        for items in all_items:
            title_tag = items.find("p", {"data-test": "product-title"})
            if not title_tag:
                continue
            title = title_tag.getText(strip=True)

            if all(re.search(rf"\b{re.escape(term)}\b", title.lower()) for term in search_terms):
                a_tag = items.find("a", {"data-test": "mms-router-link-product-image-wrapper"})
                if not a_tag:
                    continue
                new_url = a_tag.get("href")
                if not new_url:
                    continue

                if new_url.startswith("/"):
                    new_url = "https://www.mediamarkt.com.tr" + new_url
                    try:
                        response_new = requests.get(new_url, headers=self.headers, timeout=10)
                        if response_new.status_code != 200:
                            continue
                    except RequestException:
                        continue
                    soup_product = BeautifulSoup(response_new.text, "html.parser")

                    priceTag = soup_product.find("span", {"data-test": "branded-price-whole-value"})
                    if not priceTag:
                        continue
                    raw_price = priceTag.getText(strip=True)
                    parsed_price = self._parse_price(raw_price)
                    return ProductResult("MediaMarkt",title,parsed_price)

        return ProductResult("MediMarkt","EMPTY",0)

    @override
    def build_search_url(self):
        category_id = self.CATEGORIES.get(self.category_select.lower(),"")
        safe_query = urllib.parse.quote(self.users_input)
        url = f"https://www.mediamarkt.com.tr/tr/search.html?query={safe_query}&category={category_id}&&sort=currentprice+asc"
        return url
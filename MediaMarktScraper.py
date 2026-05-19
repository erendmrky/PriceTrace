import urllib.parse
import requests
from bs4 import BeautifulSoup
from typing_extensions import override
from BaseScraper import BaseScraper
from ProductResult import ProductResult


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
        response = requests.get(search_url, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")
        all_items = soup.find_all("article", {"data-test": "mms-product-card"})
        for items in all_items:
            title = items.find("p", {"data-test": "product-title"}).get_text()
            if self.users_input.lower() in title.lower():
                a_tag = items.find("a", {"data-test": "mms-router-link-product-list-item-link_mp"})
                new_url = a_tag.get("href")
                if new_url.startswith("/"):
                    new_url = "https://www.mediamarkt.com.tr" + new_url
                response_new = requests.get(new_url, headers=self.headers)
                soup_product = BeautifulSoup(response_new.text, "html.parser")

                priceTag = soup_product.find("span", {"data-test": "branded-price-whole-value"})
                raw_price = priceTag.getText(strip=True)
                parsed_price = self._parse_price(raw_price)
                result = ProductResult("MediaMarkt",title,parsed_price)
                return result
        return None

    @override
    def build_search_url(self):
        category_id = self.CATEGORIES.get(self.category_select.lower(),"")
        safe_query = urllib.parse.quote(self.users_input)
        url = f"https://www.mediamarkt.com.tr/tr/search.html?query={safe_query}&category={category_id}"
        return url
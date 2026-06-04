import urllib.parse
import re
from bs4 import BeautifulSoup
from typing_extensions import override
from BaseScraper import BaseScraper
from ProductResult import ProductResult

from camoufox.sync_api import Camoufox


class GaminggenScraper(BaseScraper):
    CATEGORIES = {
        "cpu": "islemci",
        "gpu": "ekran-karti",
        "ram": "ram-bellek",
        "motherboard": "anakart",
        "ssd": "ssd",
        "psu": "guc-kaynagi-psu"
    }

    def __init__(self, category_select, users_input):
        self.category_select = category_select
        self.users_input = users_input

    @override
    def scrape(self):
        search_url = self.build_search_url()
        page_source = ""

        try:
            with Camoufox(headless=True, humanize=True, window=(1280, 720)) as browser:
                page = browser.new_page()
                page.goto(search_url)

                page.wait_for_load_state(state="domcontentloaded")
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(5000)

                page.mouse.click(205, 330)
                page.wait_for_timeout(6000)

                if "Cloudflare" in page.title():
                    return ProductResult("Gaming.Gen.TR", "BANNED", 0)

                page_source = page.content()

        except Exception:
            return ProductResult("Gaming.Gen.TR", "TIMEOUT", 0)

        if not page_source:
            return ProductResult("Gaming.Gen.TR", "BANNED", 0)

        soup = BeautifulSoup(page_source, "html.parser")
        search_terms = self.users_input.lower().split()

        # ====================================================================
        # DURUM 1: Tekil ürün sayfasına otomatik yönlendirme kontrolü (<h1>)
        # ====================================================================
        single_title_tag = soup.find("h1", class_="product_title")
        if single_title_tag:
            title = single_title_tag.getText(strip=True)

            if all(re.search(rf"\b{re.escape(term)}\b", title.lower()) for term in search_terms):
                summary_div = single_title_tag.find_parent("div", class_="summary")
                price_tag = summary_div.find(class_="price") if summary_div else soup.find(class_="price")

                if price_tag:
                    raw_price = price_tag.getText(strip=True)
                    parsed_price = self._parse_price(raw_price)
                    return ProductResult("Gaming.Gen.TR", title, parsed_price)

        # ====================================================================
        # DURUM 2: Standart arama listesi sayfası (<h2>)
        # ====================================================================
        all_titles = soup.find_all("h2", class_="woocommerce-loop-product__title")

        for title_tag in all_titles:
            if title_tag.find_parent(class_=["related", "upsells", "cross-sells", "product-recommendations"]):
                continue

            title = title_tag.getText(strip=True)

            if all(re.search(rf"\b{re.escape(term)}\b", title.lower()) for term in search_terms):
                parent_container = title_tag.parent
                price_tag = parent_container.find("span", class_="price") if parent_container else None

                if not price_tag:
                    price_tag = title_tag.find_next("span", class_="price")

                if price_tag is not None:
                    raw_price = price_tag.getText(strip=True)
                    parsed_price = self._parse_price(raw_price)

                    return ProductResult("Gaming.Gen.TR", title, parsed_price)

        return ProductResult("Gaming.Gen.TR", "EMPTY", 0)

    @override
    def build_search_url(self):
        category_id = self.CATEGORIES.get(self.category_select.lower(), "")

        safe_query = urllib.parse.quote_plus(self.users_input.strip().lower())

        url = f"https://www.gaming.gen.tr/?kategoriler={category_id}&s={safe_query}&post_type=product&dgwt_wcas=1"
        return url
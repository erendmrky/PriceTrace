from abc import ABC, abstractmethod

class BaseScraper(ABC):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    }

    def _parse_price(self, price_str):
        if not price_str:
            return 0.0
        clean_str = price_str.replace("TL", "").replace(".", "").replace(",", ".").replace("₺","").strip()
        try:
            return float(clean_str)
        except ValueError:
            return 0.0

    @abstractmethod
    def scrape(self):
        """Scrapes the target site and returns a ProductResult object."""
        pass

    @abstractmethod
    def build_search_url(self):
        """Builds and returns the target URL based on object state."""
        pass
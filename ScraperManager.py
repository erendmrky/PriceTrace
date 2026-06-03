from ItopyaScraper import ItopyaScraper
from MediaMarktScraper import MediaMarktScraper
from IncehesapScraper import IncehesapScraper
from SinerjiScraper import SinerjiScraper
from TebilonScraper import TebilonScraper
from VatanbilgisayarScraper import VatanbilgisayarScraper


class ScraperManager:
    def __init__(self, category_select, user_input):
        self.category_select = category_select
        self.user_input = user_input

        self.scraper_classes = [
            ItopyaScraper,
            MediaMarktScraper,
            IncehesapScraper,
            SinerjiScraper,
            VatanbilgisayarScraper,
            TebilonScraper
        ]

    def run_all(self):
        result = []

        for scraper_class in self.scraper_classes:
            scraper = scraper_class(self.category_select, self.user_input)
            scrape_result = scraper.scrape()

            if scrape_result is not None:
                result.append(scrape_result)

        return result
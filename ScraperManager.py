from ItopyaScraper import ItopyaScraper
from MediaMarktScraper import MediaMarktScraper
from IncehesapScraper import IncehesapScraper
from GaminggenScraper import GaminggenScraper
from TeknobiyotikScraper import TeknobiyotikScraper
from SinerjiScraper import SinerjiScraper
from TebilonScraper import TebilonScraper
from VatanbilgisayarScraper import VatanbilgisayarScraper
from concurrent.futures import ThreadPoolExecutor, as_completed


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
            TebilonScraper,
            GaminggenScraper,
            TeknobiyotikScraper
        ]

    def run_all(self):
        results = []

        with ThreadPoolExecutor(max_workers=len(self.scraper_classes)) as executor:
            futures = {
                executor.submit(
                    cls(self.category_select, self.user_input).scrape
                ): cls for cls in self.scraper_classes
            }

            for future in as_completed(futures):
                try:
                    scrape_result = future.result()
                    if scrape_result:
                        results.append(scrape_result)
                except Exception:
                    pass

        return results
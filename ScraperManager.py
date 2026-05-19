from ItopyaScraper import ItopyaScraper
from MediaMarktScraper import MediaMarktScraper


class ScraperManager:
    def __init__(self,category_select,user_input):
        self.category_select = category_select
        self.user_input = user_input

    def run_all(self):
        result = []
        itopya_scraper = ItopyaScraper(self.category_select,self.user_input)
        itopya_result = itopya_scraper.scrape()
        if itopya_result is not None:
            result.append(itopya_result)
        mediamarkt_scraper = MediaMarktScraper(self.category_select, self.user_input)
        mediamarkt_result = mediamarkt_scraper.scrape()
        if mediamarkt_result is not None:
            result.append(mediamarkt_result)
        return result
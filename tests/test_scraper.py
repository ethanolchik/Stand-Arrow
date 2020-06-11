import unittest
import pickle
from scraper.scraper import StandScraper


class TestScraper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        configuration = {'base_url': 'https://jojowiki.com',
                         'stands_list_uri': '/List_of_Stands',
                         'stands_list_element': 'div',
                         'stands_list_attribs': {'class': 'diamond charname'}
                         }
        cls.scraper = StandScraper(config=configuration)
        with open('tests/fixtures/stand_urls', 'rb') as file:
            cls.stand_urls = pickle.load(file)

    def test_scrape_stand_urls(self):
        actual_stand_urls = self.scraper.scrape_stand_urls()
        self.assertListEqual(actual_stand_urls, self.stand_urls)

    def test_scrape_stand(self):
        # Star Platinum
        stand = self.scraper.scrape_stand(self.stand_urls[0])

    @classmethod
    def tearDownClass(cls):
        cls.scraper.stop_scraping()

        
if __name__ == '__main__':
    unittest.main()
    

from selenium import webdriver
from typing import List
from bs4 import BeautifulSoup
import config
import psycopg2
import time
import itertools


class StandScraper:

    def __init__(self, config: dict):
        self.config = config
        self.driver = webdriver.Chrome()

    def scrape_stand_urls(self) -> List[str]:
        stands_list_url = self.config['base_url'] + \
            self.config['stands_list_uri']
        try:
            self.driver.get(stands_list_url)
            source = self.driver.page_source
            soup = BeautifulSoup(source)
            stands_list = soup.findAll(self.config['stands_list_element'],
                                       self.config['stands_list_attribs'])
            stand_urls = {self.config['base_url']
                          + stand.find("a",
                                       href=True)['href']
                          for stand in stands_list}
            return sorted(list(stand_urls))
        except Exception as e:
            self.driver.close()
            self.driver.quit()
            print(e.with_traceback)

    def scrape_stand(self, stand_url: str):
        self.driver.get(stand_url)
        source = self.driver.page_source
        soup = BeautifulSoup(source)
        introduction = soup.find('meta', {'name': 'description'})['content']
        scraped_elements = [element.find_parent() for
                            element in soup.findAll('span',
                                                    {'class', 'mw-headline'})]
        filtered_elements = list(filter(lambda x: x.text not in
                                        ['Site Navigation',
                                         'Gallery', 'References'],
                                        scraped_elements))
        filtered_elements = list(filter
                                 (lambda x: x.name == 'h2', filtered_elements))
        description_as_list = []
        description_as_list.append(introduction)
        for element in filtered_elements:
            current_element = element
            section = []
            section.append(element)
            while True:
                current_element = current_element.next_sibling
                if current_element is None or current_element.name == 'h2':
                    break
                if current_element is not None:
                    section.append(current_element)
            description_as_list.append(section)

        flat_desription_list = list(
            itertools.chain.from_iterable(description_as_list))
        description = self._formatted_info(flat_desription_list)
        stand_name = soup.find('h1', {'id': 'firstHeading'}).text
        return stand_name, description

    def _formatted_info(self, flat_desription_list: list):
        string = ''
        for soup_object in flat_desription_list:
            if hasattr(soup_object, 'text'):
                string += soup_object.text
            else:
                string += str(soup_object)
        return string

    def stop_scraping(self):
        self.driver.close()
        self.driver.quit()


def insert_stand_into_db(stand_id: int, stand_name: str,
                         stand_description: str):
    stand_description_replaced = stand_description.replace("'", "''")
    stand_name = stand_name.replace("'", "''")
    print(stand_description_replaced)
    sql_statement = f"INSERT INTO Stand \
                     (stand_id, stand_name, stand_description) \
                     VALUES \
                     ({stand_id}, \
                     '{stand_name}', '{stand_description_replaced}') \
                     ON CONFLICT DO NOTHING"
    conn = psycopg2.connect(dbname=config.db["database"],
                            user=config.db["user"],
                            password=config.db["password"])
    cur = conn.cursor()
    cur.execute(sql_statement)
    conn.commit()
    cur.close()
    conn.close()
    return 0


if __name__ == "__main__":
    configuration = {'base_url': 'https://jojowiki.com',
                     'stands_list_uri': '/List_of_Stands',
                     'stands_list_element': 'div',
                     'stands_list_attribs': {'class': 'diamond charname'}
                     }
    scraper = StandScraper(config=configuration)
    stand_urls = scraper.scrape_stand_urls()
    # with open('../tests/fixtures/stand_urls', 'wb+') as file:
    #   pickle.dump(stand_urls, file)
    i = 1
    print(stand_urls)
    """
    for stand_url in stand_urls:
        time.sleep(2)
        stand_name, stand_description = scraper.scrape_stand(stand_url)
        insert_stand_into_db(i, stand_name, stand_description)
        i += 1
    """
    scraper.stop_scraping()

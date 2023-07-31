from pathlib import Path
from datetime import datetime
import scrapy


'''
Run with `$scrapy runspider argoscraper.py`
'''
class ArgoSpider(scrapy.Spider):
    name = "argo"
    date_str = datetime.today().strftime('%Y%m%d_%H%M%S')

    def start_requests(self):

        urls = [
            "https://www.languefrancaise.net/Bob/Random",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        base_data = response.css("body")[0].css("div.container-fluid")[0].css("div.row")[0].css("div")[3].css("div.fpltemplate")[0]
        # Definitions:
        terms = base_data.css("a.wikilink::text").getall()
        # Words:
        definitions = base_data.css("em::text").getall()
        page = response.url.split("/")[-3]
        filename = f"{page}-{self.date_str}.txt"
        with open(filename, 'w') as f:
            for term,defn in zip(terms, definitions):
                clean_term = term.replace("?","").replace("■ ","").strip()
                clean_defn = defn.replace("?","").replace("■ ","").strip()
                f.write(f"*{clean_term}* -- {clean_defn}\n")

        self.log(f"Saved file {filename}")

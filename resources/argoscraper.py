from pathlib import Path
from datetime import datetime
import scrapy
import json
import re
import warnings
import logging

headers = {        
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',        
    'Accept-Language': 'en-US,en;q=0.5',        
    'Connection': 'keep-alive',        
    'Cookie': 'AMCV_0D15148954E6C5100A4C98BC%40AdobeOrg=1176715910%7CMCIDTS%7C19271%7CMCMID%7C80534695734291136713728777212980602826%7CMCAAMLH-1665548058%7C7%7CMCAAMB-1665548058%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1664950458s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-19272%7CvVersion%7C5.4.0; s_ecid=MCMID%7C80534695734291136713728777212980602826; __cfruid=37ff2049fc4dcffaab8d008026b166001c67dd49-1664418998; AMCVS_0D15148954E6C5100A4C98BC%40AdobeOrg=1; s_cc=true; __cf_bm=NIDFoL5PTkinis50ohQiCs4q7U4SZJ8oTaTW4kHT0SE-1664943258-0-AVwtneMLLP997IAVfltTqK949EmY349o8RJT7pYSp/oF9lChUSNLohrDRIHsiEB5TwTZ9QL7e9nAH+2vmXzhTtE=; PHPSESSID=ddf49facfda7bcb4656eea122199ea0d',                        
    'If-Modified-Since': 'Tue, 04 May 2021 05:09:49 GMT',        
    'If-None-Match': 'W/"12c6a-5c17a16600f6c-gzip"',        
    'Sec-Fetch-Dest': 'document',        
    'Sec-Fetch-Mode': 'navigate',        
    'Sec-Fetch-Site': 'none',        
    'Sec-Fetch-User': '?1',        
    'TE': 'trailers',        
    'Upgrade-Insecure-Requests': '1',        
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'        
}

year_regex = re.compile(r'\d\d(\d\d|xx)')

def parse_css(response: scrapy.http.TextResponse):
    """Parse the css retrieved from the dictionary URL.  If the parser stops working, likely the problem is here.
    """
    base_data = response.css("body")[0].css("main#main")[0].css("div#wikitext")[0].css("div.fpltemplate")[0]
    terms = base_data.css("a::text").getall()
    definitions = base_data.css("em::text").getall()
    citations = base_data.css("span.cross::text").getall()
    years = base_data.css("ol > li > span:first-child").getall()
    years = [y if '<span style="color: green;">' in y else None for y in years]
    
    # Throw a warning if there were any suspected parsing errors
    if len(terms) != 10:
        warnings.warn(f"Unexpected number of terms {len(terms)} != 10")
    if len(definitions) != 10:
        warnings.warn(f"Unexpected number of definitions {len(definitions)} != 10")
    if len(citations) != 10:
        warnings.warn(f"Unexpected number of citations {len(citations)} != 10")
    if len(years) != 10:
        warnings.warn(f"Unexpected number of years {len(years)} != 10")
    return (terms, definitions, citations, years)

'''
Run with `$scrapy runspider argoscraper.py`
'''
class ArgoSpider(scrapy.Spider):
    name = "argo"
    date_str = datetime.today().strftime('%Y%m%d_%H%M%S')

    def __init__(self, *args, **kwargs):
        logger = logging.getLogger("scrapy")
        logger.setLevel(logging.WARNING)
        logger = logging.getLogger("asyncio")
        logger.setLevel(logging.WARNING)
        super().__init__(*args, **kwargs)

    async def start(self):

        urls = [
            "https://www.languefrancaise.net/Bob/Random",
        ]
        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def clean_year(self, year):
        if year == None:
            return None
        clean_year = year_regex.search(year)
        if clean_year == None:
            self.log("Failed to parse year: " + year)
        else:
            clean_year = clean_year.group(0)
            if 'x' in clean_year:
                clean_year = clean_year[:2] + '00s'

    def clean_and_compile_data(self, term,defn,ctn,year, skip_empty_year = False, min_num_citations = 2):
        if year == None and skip_empty_year:
            return None
        clean_ctn = int(ctn.replace("(", "").replace(")", ""))
        if clean_ctn < min_num_citations:
            return None

        clean_year = self.clean_year(year)
        clean_term = term.replace("?","").replace("■ ","").strip()
        clean_defn = defn.replace("?","").replace("■ ","").strip()
        return {
                "term": clean_term,
                "definition": clean_defn,
                "citations": clean_ctn,
                "year": clean_year
                }

    def parse(self, response):
        # CSS Parsing
        page_data = parse_css(response)
        page = response.url.split("/")[-3]
        filename = f"{page}-{self.date_str}.json"
        terms_to_add = []
        for data in zip(*page_data):
            d = self.clean_and_compile_data(*data, skip_empty_year = False, min_num_citations = 2)
            if d != None:
                terms_to_add.append(d)
        if len(terms_to_add) > 0:
            with open(filename, 'w') as fw:
                fw.seek(0)
                json.dump(terms_to_add, fw, indent=4)
                fw.truncate()
        self.log(f"Saved file {filename}")

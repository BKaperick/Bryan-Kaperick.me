import re
import os
import sys
import json
from argoscraper import ArgoSpider
from scrapy.crawler import CrawlerProcess
content_path = sys.argv[1]
force_crawl = len(sys.argv) > 2 and ('crawl' in sys.argv[2])
file_regex = re.compile(r'www\.languefrancaise\.net-.*\.json')

def pop_from_file(fname):
    lines = json.load(open(fname, 'r'))
    if not lines:
        os.remove(fname)
        return None
    line = lines[0]
    del lines[0]
    with open(fname, 'w') as fw:
        fw.seek(0)
        json.dump(lines, fw, indent=4)
        fw.truncate()
    return line

if __name__ == '__main__':
    job_done = False
    if force_crawl:
        process = CrawlerProcess()
        process.crawl(ArgoSpider)
        process.start()
    while True:
        for f in os.listdir():
            if file_regex.match(f):
                print("----------------------- matching file - starting process (" + f + ")-------------------------------")
                output = pop_from_file(f)
                if output:
                    with open (content_path, 'w') as fw:
                        fw.seek(0)
                        json.dump(output, fw, indent=4)
                        fw.truncate()
                    job_done = True
        if job_done:
            break
        else:
            process = CrawlerProcess()
            process.crawl(ArgoSpider)
            process.start()

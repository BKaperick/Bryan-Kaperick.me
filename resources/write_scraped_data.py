import re
import os
import sys
from argoscraper import ArgoSpider
from scrapy.crawler import CrawlerProcess
content_path = sys.argv[1]
file_regex = re.compile('www\.languefrancaise\.net-.*\.txt')

def pop_from_file(fname):
    lines = open(fname).readlines()
    if not lines:
        os.remove(fname)
        return None
    line = lines[0]
    del lines[0]
    open(fname, 'w').writelines(lines)
    return line

if __name__ == '__main__':
    job_done = False
    while not job_done:
        for f in os.listdir():
            if file_regex.match(f):
                output = pop_from_file(f)
                if output:
                    with open (content_path, 'w') as f:
                        f.write(output)
                        job_done = True
        if not job_done:
            process = CrawlerProcess()
            process.crawl(ArgoSpider)
            process.start()

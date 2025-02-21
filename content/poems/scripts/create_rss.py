import json
from datetime import datetime
import re
import os
import sys
sys.path.append(os.path.abspath("../../"))
from helper import *

rss_header = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>Bryan Kaperick's website</title>
    <link>http://www.bryan-kaperick.me</link>
    <description>Personal website for Bryan Kaperick</description>
    <atom:link href="https://www.bryan-kaperick.me/en/poetry/rss.xml" rel="self" type="application/rss+xml" />
"""

rss_footer = """  </channel>
</rss>
"""


def html_to_xml(text):
    return text.replace("&rsquo;", "&apos;")

def create_item(title, rawpath, desc, date):

    link = poem["rawpath"].replace("./raw/","https://www.bryan-kaperick.me/en/poetry/").replace(".txt","")
    return html_to_xml("""
    <item>
      <title>{0}</title>
      <link>{1}</link>
      <guid>{1}</guid>
      <description>{2}</description>
      <pubDate>{3}</pubDate>
    </item>
""".format(title, link, desc, date.strftime("%a, %d %b %Y %H:%M:%S GMT")))

first_line_regex = r'<div class=\"poem\"><p><span class=\"line\">(.*?)<\/span><br>'

with open("poems.json", 'r+') as fread:
    poems = [p for p in json.load(fread).items() if p[1]["author"] == "Bryan Kaperick"]
    items = []
    poems = sorted(poems, key=ordering)
    for name, poem in poems:

        description_ = re.search(first_line_regex, poem["body"])
        # Minor clean: if first line ends in '.', only add 2 more
        description = (description_.group(1) + "...").replace("....","...")

        dt_date = datetime.strptime("{0} {1}".format(poem["month"], poem["year"]), "%b %Y")
        items.append(create_item(poem["title"], poem["rawpath"], description, dt_date))

for language in ["en"]:#, "fr"]:
    lang_path = "../{0}/poetry/feed.xml".format(language)
    with open(lang_path, "w") as fw:
        fw.write(rss_header)
        fw.write("".join(items))
        fw.write(rss_footer)

import json
from datetime import datetime
import re
import os
import sys
sys.path.append(os.path.abspath("../../"))
from helper import *

rss_header = {
'en': """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>Bryan Kaperick's photos</title>
    <link>https://www.bryan-kaperick.me</link>
    <description>Photos from Bryan's life (English feed)</description>
    <language>en</language>
""",
'fr': """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>La Poesie de Bryan Kaperick</title>
    <link>https://www.bryan-kaperick.me/index_fr</link>
    <description>Des photos de la vie de Bryan (flux francais)</description>
    <language>fr</language>
"""
}

rss_footer = """  </channel>
</rss>
"""


def html_to_xml(text):
    return text.replace("&rsquo;", "&apos;")


def create_item(title, rawpath, desc, date, lang):
    link = photo["rawpath"].replace("./raw/","https://www.bryan-kaperick.me/{0}/photos/").format(lang).replace(".txt","")
    return html_to_xml("""
    <item>
      <title>{0}</title>
      <link>{1}</link>
      <guid>{1}</guid>
      <description>{2}</description>
      <pubDate>{3}</pubDate>
    </item>
""".format(title, link, desc, date.strftime("%a, %d %b %Y %H:%M:%S GMT")))

first_line_regex = r'<div class=\"photo\"><p><span class=\"line\">(.*?)<\/span><br>'

with open("photos.json", 'r+') as fread:
    photos = [p for p in json.load(fread).items()]
    items = {'en': [], 'fr': []}
    photos = sorted(photos, key=ordering)
    for name, photo in photos:
        description = photo["en"]
        dt_date = datetime.strptime("{0} {1}".format(photo["month"], photo["year"]), "%b %Y")
        items['en'].append(create_item(photo["title"], photo["rawpath"], description, dt_date, 'en'))
        items['fr'].append(create_item(photo["title"], photo["rawpath"], description, dt_date, 'fr'))

for language in ["en", "fr"]:
    lang_path = "../{0}/poetry/feed.xml".format(language)
    with open(lang_path, "w") as fw:
        fw.write(rss_header[language])
        fw.write("".join(items[language]))
        fw.write(rss_footer)

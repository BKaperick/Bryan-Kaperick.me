import json
from datetime import datetime
import re
import os
import sys
import itertools
sys.path.append(os.path.abspath("../../"))
from helper import *

rss_header = {
'en': """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>Bryan Kaperick's website</title>
    <link>https://www.bryan-kaperick.me</link>
    <description>Original content by Bryan (English feed)</description>
    <language>en</language>
""",
'fr': """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>Le Site Web de Bryan Kaperick</title>
    <link>https://www.bryan-kaperick.me/index_fr</link>
    <description>Des contenus originaux créé par Bryan (flux francais)</description>
    <language>fr</language>
"""
}

rss_footer = """  </channel>
</rss>
"""


def html_to_xml(text):
    return text.replace("&rsquo;", "&apos;")

def to_sortable_date(month, year):
    return datetime.strptime("{0} {1}".format(month, year), "%b %Y").strftime("%Y%m%d")

def to_rss_date(date):
    return datetime.strptime(date, "%Y%m%d").strftime("%a, %d %b %Y %H:%M:%S GMT")


def create_photo_json(key, photo, lang):
    link = "https://www.bryan-kaperick.me/{0}/photos/".format(lang) + key

    # the only ones without months are old photos, not a big deal if we use the proxy `order_in_year` instead
    month = photo["month"] if "month" in photo else months_reverse[photo["order_in_year"]]

    date = to_sortable_date(month, photo["year"])
    return {
        "title": photo["name"],
        "link": link,
        "desc": photo[lang],
        "date": date,
        "category": "photos"
    }

def create_poem_json(key, poem, lang):
    title = poem["title"]
    description_ = re.search(first_line_regex, poem["body"])
    # Minor clean: if first line ends in '.', only add 2 more
    desc = (description_.group(1) + "...").replace("....","...")

    date = to_sortable_date(poem["month"], poem["year"])
    link = poem["rawpath"].replace("./raw/","https://www.bryan-kaperick.me/{0}/poetry/").format(lang).replace(".txt","")
    return {
        "title": poem["title"],
        "link": link,
        "desc": desc,
        "date": date,
        "category": "poetry"
    }

def create_xml_block(json_block):
    return _create_xml_block(json_block["title"], json_block["link"], json_block["desc"], json_block["date"], json_block["category"]) 

def _create_xml_block(title, link, desc, date, category):
    return html_to_xml("""
    <item>
      <title>{0}</title>
      <link>{1}</link>
      <guid>{1}</guid>
      <description>{2}</description>
      <pubDate>{3}</pubDate>
      <category>{4}</category>
    </item>
""".format(title, link, desc, to_rss_date(date), category))

first_line_regex = r'<div class=\"poem\"><p><span class=\"line\">(.*?)<\/span><br>'

def create_combined_content_list():
    items = {'en': [], 'fr': []}
    content = []

    create_poem_content_list(items)
    create_photo_content_list(items)

    for language in ["en", "fr"]:
        lang_path = "../{0}/feed.xml".format(language)
        content = sorted(items[language], key=lambda x : x["date"])[::-1]

        with open("content_{0}.json".format(language), "w") as fw:
            fw.seek(0)
            json.dump(content, fw, indent=4)
            fw.truncate()

        with open(lang_path, "w") as fw:
            xml_content = [create_xml_block(c) for c in content]
            fw.write(rss_header[language])
            fw.write("".join(xml_content))
            fw.write(rss_footer)



    

def create_poem_content_list(items):
    with open("../poems/poems.json", 'r+') as fread:
        poems = [p for p in json.load(fread).items() if p[1]["author"] == "Bryan Kaperick"]
        #poems = sorted(poems, key=ordering)
        for name, poem in poems:
            items['en'].append(create_poem_json(name, poem, 'en'))
            items['fr'].append(create_poem_json(name, poem, 'fr'))

def create_photo_content_list(items):
    with open("../photos/photos.json", 'r+') as fread:
        photos = [p for p in json.load(fread).items()]# if p[1]["is_album"] == False]
        album_photos = set(itertools.chain.from_iterable([p[1]["photos"] for p in photos if "is_album" in p[1] and p[1]["is_album"]]))
        for name, photo in photos:
            link_name = name
            if "is_album" in photo and photo["is_album"]:
                link_name = photo["photos"][0]
            if not name in album_photos:
                items['en'].append(create_photo_json(link_name, photo, 'en'))
                items['fr'].append(create_photo_json(link_name, photo, 'fr'))

create_combined_content_list()

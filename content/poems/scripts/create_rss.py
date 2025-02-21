import json
import re

rss_header = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>Bryan Kaperick's website</title>
    <link>http://www.bryan-kaperick.me</link>
    <description>Personal website for Bryan Kaperick</description>
"""

rss_footer = """  </channel>
</rss>
"""


def create_item(title, rawpath, desc, date):

    link = poem["rawpath"].replace("./raw/","https://www.bryan-kaperick.me/en/poetry/").replace(".txt","")
    return """
    <item>
      <title>{0}</title>
      <link>{1}</link>
      <description>{2}...</description>
      <pubDate>{3}</pubDate>
    </item>
""".format(title, link, desc, date.strftime("%a, %d %b %Y %H:%M:%S GMT"))

first_line_regex = r'<div class=\"poem\"><p><span class=\"line\">(.*?)</span><br>\n<span class=\"line\">'

with open("poems.json", 'r+') as fread:
    poems = json.load(fread)
    items = []
    for name, poem in poems.items():
        if poem["author"] != "Bryan Kaperick":
            continue

        description = re.search(first_line_regex, poem["body"]).group(1)
        dt_date = datetime.strptime(f"{0} {1}".format(poem["month"], poem["year"]), "%b %Y")
        items.append(create_item(poem["title"], poem["rawpath"], description, dt_date))

with open("feed.xml", "w") as fw:
    fw.writeline(rss_header)
    fw.writeline("\n".join(items))
    fw.writeline(rss_footer)


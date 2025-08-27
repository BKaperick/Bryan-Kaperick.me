import feedparser
import json
films = feedparser.parse("https://letterboxd.com/bkapers/rss/")['entries']
with open("films.json", "w") as fw:
    fw.seek(0)
    json.dump(films, fw, indent=4)
    fw.truncate()


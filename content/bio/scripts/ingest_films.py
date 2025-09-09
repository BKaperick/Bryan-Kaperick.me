import feedparser
import json
from datetime import datetime

films = feedparser.parse("https://letterboxd.com/bkapers/rss/")['entries']
with open("films.json", "w") as fw:
    date_and_film = [(datetime.strptime(film["letterboxd_watcheddate"], "%Y-%m-%d"), film) for film in films]
    sorted_films = [f[1] for f in sorted(date_and_film, key=lambda x : x[0], reverse=True)]
    
    fw.seek(0)
    json.dump(sorted_films, fw, indent=4)
    fw.truncate()


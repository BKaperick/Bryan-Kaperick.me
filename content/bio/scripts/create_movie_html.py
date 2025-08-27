import json
import os
import sys
from math import sqrt,floor
sys.path.append(os.path.abspath("../../"))
from helper import *
from datetime import datetime
current_year = datetime.now().year


def create_film_block(key, film):
    watch_date = datetime.strptime(film["letterboxd_watcheddate"], "%Y-%m-%d")
    scaled_rating = int(float(film["letterboxd_memberrating"])*2)
    return """
    <tr>
        <td class="left"><?=$f[{0}]->letterboxd_filmtitle;?></td>
        <td><?=$f[{0}]->letterboxd_filmyear;?></td>
        <td>{1}</td>
        <td class="left">{2}</td>
    </tr>
    """.format(key, watch_date.strftime("%d %b %Y"), "█"*scaled_rating + " " + str(scaled_rating))


header = """
<table class="bordered" border=1 frame=sides cellspacing="0" cellpadding="5">
  <tr>
    <th class="border1"><?=$language["Title"];?></th>
    <th class="border1"><?=$language["Released"];?></th>
    <th class="border1"><?=$language["Watched"];?></th>
    <th class="border1" style="width: 150px;"><?=$language["Rating"];?> (1-10)</th>
  </tr>
"""
footer = """\n</table>"""

with open("films.json", "r") as fr:
    films = json.load(fr)
    blocks = []
    blocks = []
    limit = None
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])

    now = datetime.now()
    now.month
    
    for key,film in enumerate(films):
        block = create_film_block(key, film)
        blocks.append(block)
    films_html = header + "\n".join(blocks) + footer
    with open("films.html", "w") as p:
        p.write(films_html)

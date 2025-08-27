import json
import os
import sys
from math import sqrt,floor
sys.path.append(os.path.abspath("../../"))
from helper import *
from datetime import datetime
current_year = datetime.now().year

statuses = [
        "completed",
        "in-progress",
        "abandoned"
        ]

def create_book_block(key, book):
    return """
    <tr>
        <td class="left"><?=$p->{0}->title;?></td>
        <td class="left">{1}</td>
        <td class="left">{2}<?=$p->{0}->personal->finish_year;?></td>
        <td class="left" style="width: 150px;">{3} <?=$p->{0}->personal->rating;?></td>
    </tr>
    """.format(key, authors, month, "█"*int(book["personal"]["rating"]))

def date_getter(b):
    month = int(b["personal"]["finish_month"]) if "finish_month" in b["personal"] else 0
    year = 100 * int(b["personal"]["finish_year"])
    return year + month

header = """
<table class="bordered" border=1 frame=sides cellspacing="0" cellpadding="5">
  <tr>
    <th class="border1"><?=$language["Title"];?></th>
    <th class="border1"><?=$language["Author(s)"];?></th>
    <th class="border1"><?=$language["Finished"];?></th>
    <th class="border1"><?=$language["Rating"];?> (1-10)</th>
  </tr>
"""
footer = """\n</table>"""

with open("books.json", "r") as fr:
    books = json.load(fr)
    recent_blocks = []
    old_blocks = []
    limit = None
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
    books = books.items()
    ordered_books = sorted(books, key=lambda b : -date_getter(b[1]))

    now = datetime.now()
    now.month
    
    recent_books = [b[0] for b in books if (date_getter(b[1]) >= 100 * now.year) or ((date_getter(b[1]) >= 100 * (now.year - 1)) and date_getter(b[1]) % 100 >= now.month)]
    old_books = [b for b in books if not b[0] in recent_books]

    for i,(key,book) in enumerate(ordered_books):
        if book["personal"]["status"] != "completed":
            continue
        block = create_book_block(key, book)
        
        if key in recent_books:
            recent_blocks.append(block)
        else:
            old_blocks.append(block)
    
    books_html = header + "\n".join(recent_blocks) + footer
    with open("recent_books.html", "w") as p:
        p.write(books_html)
    
    books_html = header + "\n".join(old_blocks) + footer
    with open("old_books.html", "w") as p:
        p.write(books_html)

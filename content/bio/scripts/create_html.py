import json
import os
import sys
from math import sqrt,floor
sys.path.append(os.path.abspath("../../"))
from helper import *
from datetime import datetime
current_year = datetime.now().year

def create_book_block(key, book):
    authors = ", ".join([a["name"] for a in book["authors"]])
    month_ind = int(book["personal"]["finish_month"]) if "finish_month" in book["personal"] else 0
    month = months_reverse[month_ind-1] + " " if month_ind > 0 else ""
    year = int(book["personal"]["finish_year"])
    return """
    <tr>
        <td><?=$p->{0}->title;?></td>
        <td>{1}</td>
        <td>{2}<?=$p->{0}->personal->finish_year;?></td>
        <td><?=$p->{0}->personal->rating;?></td>
    </tr>
    """.format(key, authors, month)

def date_getter(b):
    month = int(b["personal"]["finish_month"]) if "finish_month" in b["personal"] else 0
    year = 100 * int(b["personal"]["finish_year"])
    return year + month

header = """
<table class="bordered" border=1 frame=sides cellspacing="0" cellpadding="5">
  <tr>
    <th class="border1">Title</th>
    <th class="border1">Author(s)</th>
    <th class="border1">Finished</th>
    <th class="border1">Rating (1-10)</th>
  </tr>
"""
footer = """\n</table>"""

with open("books.json", "r") as fr:
    books = json.load(fr)
    blocks = []
    limit = None
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
    books = books.items()
    ordered_books = sorted(books, key=lambda b : -date_getter(b[1]))
    for i,(key,book) in enumerate(ordered_books):
        block = create_book_block(key, book)
        blocks.append(block)
    books_html = header + "\n".join(blocks) + footer
    with open("books.html", "w") as p:
        p.write(books_html)

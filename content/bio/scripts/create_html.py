import json
import os
import sys
from math import sqrt,floor
sys.path.append(os.path.abspath("../../"))
from helper import *
from datetime import datetime
current_year = datetime.now().year

def wrap_book_preview_block_internal_link(key, block, links):
    internal_links = [l for l in links if l["external"] == False]
    if len(internal_links) > 0:
        return """<a href="./{0}.php">\n{1}\n</a>""".format(key, block)
    else:
        return block

ICONS = {
        "github": "../../static/external/Octicons-mark-github.svg",
        "julia-docs": "../../static/external/julia-docs.svg",
        "chrome-extension": "../../static/external/chrome-extensions.svg"
        }


def get_footer_link(key, link, i):
    icon = ICONS[link["icon"]]
    return """
        <a href=<?=$p->{0}->links[{1}]->url;?>>
          <img class="book-footer-icon" src={2}>
        </a>""".format(key, i, icon)

def get_footer_tag(key, i):
    return """<span class="book-tag"><?=$p->{0}->tags[{1}];?></span>""".format(key, i)

def create_footer_book_preview_block(key, links, tags):
    link_blocks = []
    for i,link in enumerate(links):
        link_blocks.append(get_footer_link(key, link, i))
    links_str = "\n".join(link_blocks)
    
    tag_blocks = []
    for i,tag in enumerate(tags):
        tag_blocks.append(get_footer_tag(key, i))
    tags_str = "\n".join(tag_blocks)

        
    return """<footer class="book-footer">
        <span class="book-footer-left">
        {1}
        </span>
        <span class="book-footer-right">
        <img class="invertible book-footer-link-icon" src="../../static/url-link.svg">
        {0}
        </span>
      </footer>""".format(links_str, tags_str)

def create_book_preview_block(key, book):
    head = """<div class="book-wrapper">\n"""
    header = create_header_book_preview_block(key, book)
    body = create_body_book_preview_block(key)
    footer = create_footer_book_preview_block(key, book["links"], book["tags"])
    foot = "\n</div>"

    return head + header + body + footer + foot

def create_header_book_preview_block(key, book):
    y1 = book["start_year"] 
    y2 = book["end_year"] if "end_year" in book else None
    if y2 != None and y1 == y2:
        year_str = "({0})".format(y1)
    elif y2 == None:
        year_str = "({0} - )".format(y1)
    else:
        year_str = "({0} - {1})".format(y1, y2)
    print(year_str)
    return """<header class="book-header">
      <h2 class="title book-title"><?=$p->{0}->title;?></h2>
      <h3 class="title book-title book-year">{1}</h3>
          <img class="book-icon" src=<?=$p->{0}->icon;?>>
      </header>
    """.format(key, year_str)

def create_book_block(key, book):
    authors = ", ".join([a["name"] for a in book["authors"]])
    return """<li><em><?=$p->{0}->title;?></em> &ndash; {1}</li>
    """.format(key, authors)

"""

"""

with open("books.json", "r") as fr:
    books = json.load(fr)
    blocks = []
    for key,book in books.items():
        block = create_book_block(key, book)
        blocks.append(block)
    books_html = "<ul>\n" + "\n".join(blocks) + "\n<\\ul>"
    with open("books.html", "w") as p:
        p.write(books_html)

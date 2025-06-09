import json
import os
import sys
from math import sqrt,floor
sys.path.append(os.path.abspath("../../"))
from helper import *
from datetime import datetime
current_year = datetime.now().year

def wrap_project_preview_block_internal_link(key, block, links):
    internal_links = [l for l in links if l["external"] == False]
    if len(internal_links) > 0:
        return """<a href="./{0}.php">\n{1}\n</a>""".format(key, block)
    else:
        return block

ICONS = {
        "github": "../../static/external/Octicons-mark-github.svg",
        "chrome-extension": "../../static/external/chrome-extensions.svg"
        }


def get_footer_link(key, link, i):
    icon = ICONS[link["icon"]]
    return """
        <a href=<?=$p->{0}->links[{1}]->url;?>>
          <img class="project-footer-icon" src={2}>
        </a>""".format(key, i, icon)

def get_footer_tag(key, i):
    return """<span class="project-tag"><?=$p->{0}->tags[{1}];?></span>""".format(key, i)

def create_footer_project_preview_block(key, links, tags):
    link_blocks = []
    for i,link in enumerate(links):
        link_blocks.append(get_footer_link(key, link, i))
    links_str = "\n".join(link_blocks)
    
    tag_blocks = []
    for i,tag in enumerate(tags):
        tag_blocks.append(get_footer_tag(key, i))
    tags_str = "\n".join(tag_blocks)

        
    return """<footer class="project-footer">
        <span class="project-footer-left">
        {1}
        </span>
        <span class="project-footer-right">
        <img class="invertible project-footer-link-icon" src="../../static/url-link.svg">
        {0}
        </span>
      </footer>""".format(links_str, tags_str)

def create_project_preview_block(key, project):
    head = """<div class="project-wrapper">\n"""
    header = create_header_project_preview_block(key, project)
    body = create_body_project_preview_block(key)
    footer = create_footer_project_preview_block(key, project["links"], project["tags"])
    foot = "\n</div>"

    return head + header + body + footer + foot

def create_header_project_preview_block(key, project):
    y1 = project["start_year"] 
    y2 = project["end_year"] if "end_year" in project else None
    if y2 != None and y1 == y2:
        year_str = "({0})".format(y1)
    elif y2 == None:
        year_str = "({0} - )".format(y1)
    else:
        year_str = "({0} - {1})".format(y1, y2)
    print(year_str)
    return """<header class="project-header">
      <h2 class="title project-title"><?=$p->{0}->title;?></h2>
      <h3 class="title project-title project-year">{1}</h3>
          <img class="project-icon" src=<?=$p->{0}->icon;?>>
      </header>
    """.format(key, year_str)

def create_body_project_preview_block(key):
    return """
      
      <div class="project-content project-tagline">
        <?=$p->{0}->$lang;?>
      </div>
    """.format(key)

"""

"""

with open("projects.json", "r") as fr:
    projects = json.load(fr)
    previews = []
    for key,project in projects.items():
        links = project["links"]
        block = create_project_preview_block(key, project)
        block = wrap_project_preview_block_internal_link(key, block, links)
        previews.append((block, project["order"]))
    sorted_previews = [p[0] for p in sorted(previews, key= lambda x : x[1])]
    projects_html = "\n\n".join(sorted_previews)
    with open("projects.html", "w") as p:
        p.write(projects_html)

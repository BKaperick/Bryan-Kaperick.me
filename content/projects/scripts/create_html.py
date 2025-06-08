import json
import os
import sys
from math import sqrt,floor
sys.path.append(os.path.abspath("../../"))
from helper import *


def create_project_preview_block(key):
    return """
  <a href="./{0}.php">
    <div class="project-wrapper">
      <header class="project-header">
      <h2 class="title project-title"><?=$p->{0}->title;?></h2>
          <img class="project-icon" src=<?=$p->{0}->icon;?>>
      </header>
      <div class="content project-tagline">
      <?=$p->{0}->$lang;?>...
      </div>
    </div>
  </a>""".format(key)


with open("projects.json", "r") as fr:
    projects = json.load(fr)
    previews = []
    for key,project in projects.items():
        previews.append((create_project_preview_block(key), project["order"]))
    sorted_previews = [p[0] for p in sorted(previews, key= lambda x : x[1])]
    projects_html = "\n\n".join(sorted_previews)
    with open("projects.html", "w") as p:
        p.write(projects_html)

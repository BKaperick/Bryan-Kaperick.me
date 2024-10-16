import os
import sys
sys.path.append(os.path.abspath("../../"))
from helper import *
import json
attribution_blocks = []
"""
    "american_coffee": {
        "name": "Coffee",
        "author": "Bilicube Studio",
        "image": "../../static/american-coffee.svg",
        "link": "https://thenounproject.com/icon/coffee-7286442/",
        "repository": "Noun Project",
        "license": "CC BY 3.0"
    },
"""
def get_block(key):
    return """<p><em><?=$p->{0}->name;?></em> &ndash; <?=$p->{0}->author;?>
    {1}</p>
    <blockquote>
    <?=$p->{0}->body;?>
    </blockquote>""".format(key, "<em><br /><p>&nbsp;&nbsp;&nbsp;&nbsp;<?=$p->{0}->subtitle;?></em></p>".format(key) if subtitle else "")

with open("attributions.json", "r") as fr:
    attrs = json.load(fr)
    for key,attr in attrs.items():
        b

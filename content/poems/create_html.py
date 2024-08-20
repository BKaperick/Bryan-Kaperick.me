import os
import sys
sys.path.append(os.path.abspath("../../"))
from helper import *
import json
poem_blocks = []

def get_bryan_block(key):
    return """<p><em><?=$p->{0}->title;?></em> &ndash; <?=$language[$p->{0}->month];?> <?=$p->{0}->year;?></p>
    <blockquote>
    <?=$p->{0}->body;?>
    </blockquote>""".format(key)

def get_insp_block(key, subtitle = False):
    return """<p><em><?=$p->{0}->title;?></em> &ndash; <?=$p->{0}->author;?>
    {1}</p>
    <blockquote>
    <?=$p->{0}->body;?>
    </blockquote>""".format(key, "<em><br /><p>&nbsp;&nbsp;&nbsp;&nbsp;<?=$p->{0}->subtitle;?></em></p>".format(key) if subtitle else "")

with open("poems.json", "r") as fr:
    poems = json.load(fr)
    for key,poem in poems.items():
        block = get_bryan_block(key) if poem['author'] == 'Bryan Kaperick' else get_insp_block(key, 'subtitle' in poem.keys())
        poem_blocks.append((block, poem))

with open("poems_inspiration.html", "w") as f_insp:
    poems_insp = [p for p in poem_blocks if p[1]['author'] != "Bryan Kaperick"]
    f_insp.write("\n\n".join([x[0] for x in poems_insp]))

with open("poems2024.html", "w") as f24:
    poems24 = [p for p in poem_blocks if p[1]['author'] == "Bryan Kaperick" and int(p[1]['year']) == 2024]
    f24.write("\n\n".join([x[0] for x in sorted(poems24, key=ordering)]))

with open("poems2023.html", "w") as f23:
    poems23 = [p for p in poem_blocks if p[1]['author'] == "Bryan Kaperick" and int(p[1]['year']) == 2023]
    f23.write("\n\n".join([x[0] for x in sorted(poems23, key=ordering)]))

with open("poems2022.html", "w") as f22:
    poems22 = [p for p in poem_blocks if p[1]['author'] == "Bryan Kaperick" and int(p[1]['year']) <= 2022]
    f22.write("\n\n".join([x[0] for x in sorted(poems22, key=ordering)]))

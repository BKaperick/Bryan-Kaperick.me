import os
import sys
sys.path.append(os.path.abspath("../../"))
from helper import *
import json
poem_blocks = []

def get_bryan_block(key, block_path):
    return """
<link rel="shortcut icon" type="image/x-icon" href="/static/favicon.ico">
<link rel="icon" type="image/x-icon" href="/static/favicon.ico">
<link rel="apple-touch-icon" href="/static/favicon.ico">
<link rel="stylesheet" href="/style.css">
<p><em><?=$p->{0}->title;?></em> &ndash; <?=$language[$p->{0}->month];?> <?=$p->{0}->year;?></p>
    <blockquote>
    <?=$p->{0}->body;?>
    </blockquote>""".format(key, block_path)

def get_insp_block(key, subtitle = False):
    return """<p><em><?=$p->{0}->title;?></em> &ndash; <?=$p->{0}->author;?>
    {1}</p>
    <blockquote>
    <?=$p->{0}->body;?>
    </blockquote>""".format(key, "<em><br /><p>&nbsp;&nbsp;&nbsp;&nbsp;<?=$p->{0}->subtitle;?></em></p>".format(key) if subtitle else "")

def wrap_block_in_link(block, poem, link):
    wrapped_block = """<a href="<?="/poems/{0}"?>" style="text-decoration:none">{1}
</a>""".format(link, block)
    return (wrapped_block, poem, link)

with open("poems.json", "r") as fr:
    poems = json.load(fr)
    for key,poem in poems.items():
        if poem['author'] == 'Bryan Kaperick':
            block_path = poem['rawpath'].replace(".txt", ".php").replace("./raw/", "")
            block = get_bryan_block(key, block_path)
        else:
            block_path = None
            block = get_insp_block(key, 'subtitle' in poem.keys())
        poem_blocks.append((block, poem, block_path))

with open("poems_inspiration.html", "w") as f_insp:
    poems_insp = [p for p in poem_blocks if p[1]['author'] != "Bryan Kaperick"]
    f_insp.write("\n\n".join([x[0] for x in poems_insp]))

with open("poems2024.html", "w") as f24:
    poems24 = [wrap_block_in_link(*p) for p in poem_blocks if p[1]['author'] == "Bryan Kaperick" and int(p[1]['year']) == 2024]
    f24.write("\n\n".join([x[0] for x in sorted(poems24, key=ordering)]))

with open("poems2023.html", "w") as f23:
    poems23 = [wrap_block_in_link(*p) for p in poem_blocks if p[1]['author'] == "Bryan Kaperick" and int(p[1]['year']) == 2023]
    f23.write("\n\n".join([x[0] for x in sorted(poems23, key=ordering)]))

with open("poems2022.html", "w") as f22:
    poems22 = [wrap_block_in_link(*p) for p in poem_blocks if p[1]['author'] == "Bryan Kaperick" and int(p[1]['year']) <= 2022]
    f22.write("\n\n".join([x[0] for x in sorted(poems22, key=ordering)]))

for block,poem,php_path in poem_blocks:
    if 'rawpath' in poem:
        html_path = "./blocks/" + php_path.replace(".php", ".html")
        with open(html_path, "w") as f:
            f.write(block)
        with open(php_path, "w") as f:
            f.write("""<?php 
$lang = $_GET["lang"] ?? "en";
global $language;
require_once($_SERVER['DOCUMENT_ROOT']."/view/Language/lang.".$lang.".php");

$string = file_get_contents($_SERVER['DOCUMENT_ROOT']."/poems/poems.json");
$p = json_decode($string);
global $p;
include($_SERVER['DOCUMENT_ROOT']."/poems/{0}");
?> 
""".format(html_path))

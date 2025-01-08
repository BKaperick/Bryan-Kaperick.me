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

def get_bryan_block_with_audio(key):
    return """<p><em><?=$p->{0}->title;?></em> &ndash; <?=$language[$p->{0}->month];?> <?=$p->{0}->year;?></p>
    <blockquote>
    <?=$p->{0}->body;?>
    </blockquote>
    <audio controls src="<?=$p->{0}->audiopath;?>"></audio>
    """.format(key)

def get_insp_block(key, subtitle = False):
    return """<p><em><?=$p->{0}->title;?></em> &ndash; <?=$p->{0}->author;?>
    {1}</p>
    <blockquote>
    <?=$p->{0}->body;?>
    </blockquote>""".format(key, "<em><br /><p>&nbsp;&nbsp;&nbsp;&nbsp;<?=$p->{0}->subtitle;?></em></p>".format(key) if subtitle else "")

def wrap_block_in_link(block, poem, link, _):
    wrapped_block = """<a href="<?="/" . $lang . "/poetry/{0}"?>" style="text-decoration:none">{1}
</a>""".format(link, block)
    return (wrapped_block, poem, link)

with open("poems.json", "r") as fr:
    poems = json.load(fr)
    for key,poem in poems.items():
        audio_block = None
        if poem['author'] == 'Bryan Kaperick':
            block_path = poem['rawpath'].replace(".txt", ".php").replace("./raw/", "")
            block = get_bryan_block(key)
            if "audiopath" in poem.keys():
                audio_block = get_bryan_block_with_audio(key)
        else:
            block_path = None
            block = get_insp_block(key, 'subtitle' in poem.keys())
        poem_blocks.append((block, poem, block_path, audio_block))

with open("poems_inspiration.html", "w") as f_insp:
    poems_insp = [p for p in poem_blocks if p[1]['author'] != "Bryan Kaperick"]
    f_insp.write("\n\n".join([x[0] for x in poems_insp]))

with open("poems2025.html", "w") as f25:
    poems25 = [wrap_block_in_link(*p) for p in poem_blocks if p[1]['author'] == "Bryan Kaperick" and int(p[1]['year']) == 2025]
    f25.write("\n\n".join([x[0] for x in sorted(poems25, key=ordering)]))

with open("poems2024.html", "w") as f24:
    poems24 = [wrap_block_in_link(*p) for p in poem_blocks if p[1]['author'] == "Bryan Kaperick" and int(p[1]['year']) == 2024]
    f24.write("\n\n".join([x[0] for x in sorted(poems24, key=ordering)]))

with open("poems2023.html", "w") as f23:
    poems23 = [wrap_block_in_link(*p) for p in poem_blocks if p[1]['author'] == "Bryan Kaperick" and int(p[1]['year']) == 2023]
    f23.write("\n\n".join([x[0] for x in sorted(poems23, key=ordering)]))

with open("poems2022.html", "w") as f22:
    poems22 = [wrap_block_in_link(*p) for p in poem_blocks if p[1]['author'] == "Bryan Kaperick" and int(p[1]['year']) <= 2022]
    f22.write("\n\n".join([x[0] for x in sorted(poems22, key=ordering)]))

for block,poem,php_path,audio_block in poem_blocks:
    if 'rawpath' in poem:
        html_path = "./blocks/" + php_path.replace(".php", ".html")
        with open(html_path, "w") as f:
            # We only write the audio block if an audio exists, and only on the single-poem page
            block_to_write = block if audio_block == None else audio_block
            f.write(block_to_write)

        for language in ["en", "fr"]:
            lang_php_path = "../{0}/poetry/{1}".format(language, php_path)
            with open(lang_php_path, "w") as f:
                f.write("""<?php 
include($_SERVER['DOCUMENT_ROOT']."/poems/minimal_poem_header.php");
include($_SERVER['DOCUMENT_ROOT']."/{0}/minimal_header.html");
include($_SERVER['DOCUMENT_ROOT']."/poems/{1}");
?> 
""".format(language, html_path))

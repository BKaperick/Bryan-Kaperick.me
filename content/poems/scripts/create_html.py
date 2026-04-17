import os
import sys

sys.path.append(os.path.abspath("../../"))
from helper import ordering
import json
from datetime import datetime

current_year = datetime.now().year

poem_blocks = []


def get_bryan_block(key, is_dedicated_page: bool, with_audio: bool) -> str:
    # class is used adjust font size separately from the main poems page
    div_class = "dedicated-poem-page" if is_dedicated_page else "poem"
    audio = (
        f"""<audio controls src="<?=$p->{key}->audiopath;?>"></audio>\n"""
        if with_audio
        else "\n"
    )
    return f"""<div class="{div_class}">
    <p><em><?=$p->{key}->title;?></em> &ndash; <?=$language[$p->{key}->month];?> <?=$p->{key}->year;?></p>
    <blockquote>
    <?=$p->{key}->body;?>
    </blockquote>
    {audio}
    </div>"""


def get_insp_block(key, subtitle=False) -> str:
    return """<p><em><?=$p->{0}->title;?></em> &ndash; <?=$p->{0}->author;?>
    {1}</p>
    <blockquote>
    <?=$p->{0}->body;?>
    </blockquote>""".format(
        key,
        "<em><br /><p>&nbsp;&nbsp;&nbsp;&nbsp;<?=$p->{0}->subtitle;?></em></p>".format(
            key
        )
        if subtitle
        else "",
    )


def wrap_block_in_link(main_page_block, poem, link, _):
    wrapped_block = f"""<a href="<?="/" . $lang . "/poetry/{link}"?>" style="text-decoration:none">{main_page_block}
</a>"""
    return (wrapped_block, poem, link)


with open("poems.json", "r") as fr:
    poems = json.load(fr)
    for key, poem in poems.items():
        dedicated_page_block = None
        if poem["author"] == "Bryan Kaperick":
            block_path = poem["rawpath"].replace(".txt", ".php").replace("./raw/", "")

            # Currently, the only difference is that the dedicated page includes the audio.
            main_page_block = get_bryan_block(key, False, False)
            dedicated_page_block = get_bryan_block(
                key, True, "audiopath" in poem.keys()
            )
        else:
            block_path = None
            main_page_block = get_insp_block(key, "subtitle" in poem.keys())
        poem_blocks.append((main_page_block, poem, block_path, dedicated_page_block))

with open("poems_inspiration.generated.html", "w") as f_insp:
    poems_insp = [p for p in poem_blocks if p[1]["author"] != "Bryan Kaperick"]
    f_insp.write("\n\n".join([x[0] for x in poems_insp]))

min_single_year = 2022

for year in range(min_single_year + 1, current_year + 1):
    with open(f"poems{year}.generated.html", "w") as f_year:
        poems_year = [
            wrap_block_in_link(*p)
            for p in poem_blocks
            if p[1]["author"] == "Bryan Kaperick" and int(p[1]["year"]) == year
        ]
        f_year.write("\n\n".join([x[0] for x in sorted(poems_year, key=ordering)]))

# Note: for the min year, we use <= rather than strict =.
with open(f"poems{min_single_year}.generated.html", "w") as f_year:
    poems_year = [
        wrap_block_in_link(*p)
        for p in poem_blocks
        if p[1]["author"] == "Bryan Kaperick" and int(p[1]["year"]) <= min_single_year
    ]
    f_year.write("\n\n".join([x[0] for x in sorted(poems_year, key=ordering)]))

for main_page_block, poem, php_path, dedicated_page_block in poem_blocks:
    if "rawpath" in poem:
        html_path = "./blocks/" + php_path.replace(".php", ".generated.html")
        with open(html_path, "w") as f:
            f.write(dedicated_page_block)

        for language in ["en", "fr"]:
            lang_php_path = "../{0}/poetry/{1}".format(language, php_path)
            with open(lang_php_path, "w") as f:
                f.write(
                    """<?php 
include($_SERVER['DOCUMENT_ROOT']."/poems/minimal_poem_header.php");
include($_SERVER['DOCUMENT_ROOT']."/{0}/minimal_header.html");
include($_SERVER['DOCUMENT_ROOT']."/poems/{1}");
?> 
""".format(language, html_path)
                )

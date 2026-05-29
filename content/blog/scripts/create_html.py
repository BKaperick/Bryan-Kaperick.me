import os
import sys

sys.path.append(os.path.abspath("../../"))
from helper import ordering
import json
from datetime import datetime

current_year = datetime.now().year

post_blocks = []


def get_block(key, is_dedicated_page: bool, with_audio: bool) -> str:
    # class is used adjust font size separately from the main posts page
    div_class = "dedicated-post-page" if is_dedicated_page else "main-post-page"
    audio = (
        f"""<audio controls src="<?=$p->{key}->audiopath;?>"></audio>\n"""
        if with_audio
        else ""
    )
    return f"""<div class="{div_class}" id="{key}">
    <p class="post-title"><em><?=$p->{key}->title;?></em> &ndash; <?=$language[$p->{key}->month];?> <?=$p->{key}->year;?></p>
    <blockquote>
    <?=$p->{key}->body;?>
    </blockquote>
    {audio}</div>"""


def get_insp_block(key, subtitle=False) -> str:
    return """<p class="post-title"><em><?=$p->{0}->title;?></em> &ndash; <?=$p->{0}->author;?>
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


def wrap_block_in_link(main_page_block, post, link, _):
    wrapped_block = f"""<a href="<?="/" . $lang . "/blog-posts/{link}"?>" style="text-decoration:none">{main_page_block}
</a>"""
    return (wrapped_block, post, link)


with open("posts.json", "r") as fr:
    posts = json.load(fr)
    for key, post in posts.items():
        dedicated_page_block = None
        if post["author"] == "Bryan Kaperick":
            block_path = post["rawpath"].replace(".txt", ".php").replace("./raw/", "")

            # Currently, the only difference is that the dedicated page includes the audio.
            main_page_block = get_block(key, False, False)
            dedicated_page_block = get_block(key, True, "audiopath" in post.keys())
        else:
            block_path = None
            main_page_block = get_insp_block(key, "subtitle" in post.keys())
        post_blocks.append((main_page_block, post, block_path, dedicated_page_block))

with open("posts_inspiration.generated.html", "w") as f_insp:
    posts_insp = [p for p in post_blocks if p[1]["author"] != "Bryan Kaperick"]
    f_insp.write("\n\n".join([x[0] for x in posts_insp]))

min_single_year = 2022

for year in range(min_single_year + 1, current_year + 1):
    with open(f"posts{year}.generated.html", "w") as f_year:
        posts_year = [
            wrap_block_in_link(*p)
            for p in post_blocks
            if p[1]["author"] == "Bryan Kaperick" and int(p[1]["year"]) == year
        ]
        f_year.write("\n\n".join([x[0] for x in sorted(posts_year, key=ordering)]))

# Note: for the min year, we use <= rather than strict =.
with open(f"posts{min_single_year}.generated.html", "w") as f_year:
    posts_year = [
        wrap_block_in_link(*p)
        for p in post_blocks
        if p[1]["author"] == "Bryan Kaperick" and int(p[1]["year"]) <= min_single_year
    ]
    f_year.write("\n\n".join([x[0] for x in sorted(posts_year, key=ordering)]))

for main_page_block, post, php_path, dedicated_page_block in post_blocks:
    if "rawpath" in post:
        html_path = "./blocks/" + php_path.replace(".php", ".generated.html")
        with open(html_path, "w") as f:
            f.write(dedicated_page_block)

        for language in ["en", "fr"]:
            lang_php_path = "../{0}/blog-posts/{1}".format(language, php_path)
            with open(lang_php_path, "w") as f:
                f.write(
                    """<?php 
include($_SERVER['DOCUMENT_ROOT']."/blog/minimal_post_header.php");
include($_SERVER['DOCUMENT_ROOT']."/{0}/minimal_header.html");
include($_SERVER['DOCUMENT_ROOT']."/blog/{1}");
?> 
""".format(language, html_path)
                )

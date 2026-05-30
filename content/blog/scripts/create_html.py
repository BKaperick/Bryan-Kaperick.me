import os
import sys

sys.path.append(os.path.abspath("../../"))
from helper import ordering
import json
from datetime import datetime

current_year = datetime.now().year

post_blocks = []


def get_block(key, is_dedicated_page: bool) -> str:
    # class is used adjust font size separately from the main posts page
    div_class = "dedicated-post-page" if is_dedicated_page else "main-post-page"
    return f"""<div class="{div_class}" id="{key}">
    <p class="post-title"> <?=$p->{key}->day;?> <?=$language[$p->{key}->month];?> <?=$p->{key}->year;?></p>
    <blockquote>
    <em><?=$p->{key}->title;?></em>
    <br>
    <?=$p->{key}->body;?>
    </blockquote>
    </div>"""


def wrap_block_in_link(main_page_block, post, link, _):
    wrapped_block = f"""<a href="<?="/" . $lang . "/blog-posts/{link}"?>" style="text-decoration:none">{main_page_block}
</a>"""
    return (wrapped_block, post, link)


with open("posts.json", "r") as fr:
    posts = json.load(fr)
    for key, post in posts.items():
        block_path = post["rawpath"].replace(".txt", ".php").replace("./raw/", "")

        # Currently, the only difference is that the dedicated page includes the audio.
        main_page_block = get_block(key, False)
        post_blocks.append((main_page_block, post, block_path, main_page_block))

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

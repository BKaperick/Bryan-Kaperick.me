import json
import os
import sys
from math import sqrt, floor
from datetime import datetime

sys.path.append(os.path.abspath("../../"))
from create_leaderboard import get_leaderboard, get_leaderboard_winner
from helper import order_photos

photo_blocks = []


def get_empty_grid(photo_count: int) -> str:
    """Define the grid for displaying an album on the main photos page."""
    rows = floor(sqrt(photo_count))
    columns = photo_count // rows
    rows_with_extra = photo_count % rows

    elem = """"""
    count = 0
    for r in range(rows):
        elem += '<div class="photorow">\n'
        for c in range(columns + int(r < rows_with_extra)):
            elem += f'<div class="photocolumn"> {{{str(count)}}} </div>\n'
            count += 1
        elem += "</div>\n"
    return elem


def get_filled_grid(photos: list[str]) -> str:
    return get_empty_grid(len(photos)).format(*photos)


def get_photo_captioned_figure(key, subdir) -> str:
    """
    Photo in its dedicated page, not within an album.
    Figure with caption.  If `album_key` is given AND `use_photo_caption` is True,
    then we use the description from the album instead
    """
    caption = f"<?=$p->{key}->$lang;?> ~ <?=$p->{key}->year;?>"
    file_suffix = ".webp" if subdir == "lowres" else ""
    image_class = (
        "image main-page-photo-block" if subdir == "lowres" else "single-image"
    )
    image = f'<img src=<?="/photos/{subdir}/". $p->{key}->name . "{file_suffix}";?> alt="{caption}">'
    return get_figure(
        image_class,
        key,
        image,
        caption,
    )


def get_figure(classes, id, content: str, caption) -> str:
    id_part = f'id="{id}"' if id else ""
    return "\n".join(
        [
            f'<figure class="{classes}" {id_part}>',
            content,
            '<figcaption class="photo-caption">',
            f"    {caption}",
            "</figcaption>",
            "</figure>",
        ]
    )


def get_photo_captioned_figure_with_previous_next(
    key, use_photo_caption=True, album_key=None, prev_file=None, next_file=None
):
    """
    Figure with caption.  If `album_key` is given AND `use_photo_caption` is True,
    then we use the description from the album instead
    """
    subdir = "raw"
    caption_key = key if use_photo_caption else album_key
    caption = f"<?=$p->{caption_key}->$lang;?> ~ <?=$p->{key}->year;?>"
    prev_link = (
        f"""<a class="prev_link" href="<?="./{prev_file}.generated.php";?>"><?=$language['Previous']?></a>"""
        if prev_file
        else ""
    )
    next_link = (
        f"""<a class="next_link" href="<?="./{next_file}.generated.php";?>"><?=$language['Next']?></a>"""
        if next_file
        else ""
    )

    image = f'<img src=<?="/photos/{subdir}/" . $p->{key}->name;?> alt="{caption}">'
    full_caption = f"{prev_link}\n{caption}\n{next_link}"

    return get_figure("single-image", None, image, full_caption)


def get_dedicated_page_photo_in_album(
    key, has_caption: bool, album_key: str, photo_prev, photo_next
):
    prev_file_name = (
        photo_prev["name"].replace(".jpg", "") if photo_prev is not None else None
    )
    next_file_name = (
        photo_next["name"].replace(".jpg", "") if photo_next is not None else None
    )
    return get_photo_captioned_figure_with_previous_next(
        key,
        has_caption,
        album_key,
        prev_file_name,
        next_file_name,
    )


def get_main_page_photo_block(key, file_name):
    """A photo on the main photo page, not contained within an album."""
    return "\n".join(
        [
            f'<a id="{key}" href="<?="/" . $lang . "/photos/{file_name}.generated.php";?>">',
            get_photo_captioned_figure(key, "lowres"),
            "</a>",
        ]
    )


def get_photo_block_in_album(key, file_name):
    """A Photo in its dedicated page, within the context of an album."""
    caption = f"<?=$p->{key}->$lang;?>"
    image = f'<img class="albumimage" src=<?="/photos/lowres/" . $p->{key}->name . ".webp";?> alt="{caption}">'
    return "\n".join(
        [
            '<span style="color:grey">',
            f'<a href="<?="/" . $lang . "/photos/{file_name}.generated.php";?>">',
            get_figure("albumimage", None, image, caption),
            "</a></span>",
        ]
    )


def generate_leaderboard():

    #
    # HTML Blocks
    #
    two_row_block = """    <tr> 
        <td>{0}</td>
        <td>{1}</td>
    </tr>\n"""

    one_table_header = """<table class="bordered" border=1 frame=sides style="float: left; max-width: 250px; margin: 25px">
        <th class="border1" colspan=2><?=$language['{0}'];?></th>\n"""

    header = """
    <details>
      <summary><h3><?=$language['leaderboard'];?></h3>
    </summary>
    <div class="clearfix">"""

    footer = """</details></div>"""

    # all-time table filling
    alltime_table = one_table_header.format("All-time Leaderboard")
    ranked, cnt = get_leaderboard()
    for i, (person, cnt) in enumerate(ranked[::-1]):
        block = two_row_block.format(i + 1, person)
        alltime_table += block
        if i + 1 >= 10:
            break
    alltime_table += "</table>"

    # historical table filling
    history_table = one_table_header.format("Previous Winners")
    current_year = datetime.now().year
    for year in range(current_year - 9, current_year + 1)[::-1]:
        winner, winner_metric = get_leaderboard_winner(year, metric="inv_weight")
        year = str(year) + "*" if year == current_year else year
        block = two_row_block.format(year, winner)
        history_table += block
    history_table += "</table>\n"
    history_table += "* year in progress"

    # Assemble the data
    data = [header]
    data.append(alltime_table)
    data.append(history_table)
    data.append(footer)
    return "\n".join(data)


def fill_album_prev_next_links(
    key,
    photo,
    photo_key_to_album_key: dict[str, str],
    photo_key_to_previous: dict[str, str | None],
    photo_key_to_next: dict[str, str | None],
):
    for i, subkey in enumerate(photo["photos"]):
        photo_key_to_album_key[subkey] = key
        # Used to assign the 'Previous' and 'Next links on the single-photo page when the photo is part of an album
        photo_key_to_previous[subkey] = None if i == 0 else photo["photos"][i - 1]
        photo_key_to_next[subkey] = (
            None if i == len(photo["photos"]) - 1 else photo["photos"][i + 1]
        )


def get_main_page_album_block(
    album_key: str,
    photo,
) -> str:
    """Get album block for main page."""
    photo_blocks: list[str] = []
    for subkey in photo["photos"]:
        sub_file_name = photos[subkey]["name"].replace(".jpg", "")
        sub_block = get_photo_block_in_album(subkey, sub_file_name)
        photo_blocks.append(sub_block)

    images_elem = get_filled_grid(photo_blocks)
    caption = f"<?=$p->{album_key}->$lang;?> ~ <?=$p->{album_key}->year;?>"

    figure = get_figure("album", album_key, images_elem, caption)

    return "\n".join(
        [
            f'<div class="album main-page-photo-block" id="{album_key}">',
            figure,
            "</div>",
        ]
    )


def write_dedicated_photo_pages(photos) -> None:
    photo_key_to_album_key: dict[str, str] = {}
    photo_key_to_previous: dict[str, str | None] = {}
    photo_key_to_next: dict[str, str | None] = {}

    for key, photo in photos.items():
        if photo.get("is_album"):
            fill_album_prev_next_links(
                key,
                photo,
                photo_key_to_album_key,
                photo_key_to_previous,
                photo_key_to_next,
            )

    for key, photo in photos.items():
        file_name = photo["name"].replace(".jpg", "")
        # DEDICATED PAGES

        # The idea is that if the photo is (1) contained in an album and (2) doesn't have its own description,
        # then on the single-image page, we use the album caption rather than leaving it at "~ [year]"
        if key in photo_key_to_album_key:
            ded_block = get_dedicated_page_photo_in_album(
                key,
                photo["en"] or photo["fr"],
                photo_key_to_album_key[key],
                photos.get(photo_key_to_previous[key]),
                photos.get(photo_key_to_next[key]),
            )
        else:
            ded_block = get_photo_captioned_figure(key, "raw")

        html_path = "./raw_with_label/" + file_name + ".generated.html"
        with open(html_path, "w") as f:
            f.write(ded_block)
        for language in ["en", "fr"]:
            php_path = "../{0}/photos/{1}.generated.php".format(language, file_name)
            with open(php_path, "w") as f:
                f.write(
                    f"""<?php 
include($_SERVER['DOCUMENT_ROOT']."/photos/minimal_photo_header.php");
include($_SERVER['DOCUMENT_ROOT']."/{language}/minimal_header.html");
include($_SERVER['DOCUMENT_ROOT']."/photos/{html_path}");
?> 
"""
                )


def write_main_page_photo_page(photos):
    """Generate and write the main page html blocks.  There are two cases:
    1. The photo is contained within an album, so it is printed in a grid along with the other photos from the album
    2. The photo is not within an album, so we print it by itself on the main page."""
    album_photos = [
        photo
        for album_photo in photos.values()
        for photo in album_photo.get("photos", [])
        if album_photo.get("is_album")
    ]
    # Get single-image pages (stored in raw_with_label)
    for key, photo in photos.items():
        file_name = photo["name"].replace(".jpg", "")

        # MAIN PAGE

        # The element is an album
        if photo.get("is_album"):
            main_block = get_main_page_album_block(
                key,
                photo,
            )
            photo_blocks.append((main_block, photo))

        # Photo is not contained in any album, so just print it on main photos page
        elif key not in album_photos:
            main_block = get_main_page_photo_block(key, file_name)
            photo_blocks.append((main_block, photo))

    with open("photos.generated.html", "w") as f:
        f.write(generate_leaderboard())
        f.write("\n\n\n")
        f.write("\n\n".join([x[0] for x in sorted(photo_blocks, key=order_photos)]))
        f.write("\n")


with open("photos.json", "r") as fw:
    photos = json.load(fw)
    write_dedicated_photo_pages(photos)
    write_main_page_photo_page(photos)

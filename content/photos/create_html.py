import json
import os
import sys
from math import sqrt,floor
sys.path.append(os.path.abspath("../../"))
from helper import *

photo_blocks = []

def get_grid(photo_count):
    rows = floor(sqrt(photo_count))
    columns = photo_count // rows
    rows_with_extra = photo_count % rows
    
    elem = """"""
    count = 0
    for r in range(rows):
        elem += '<div class="photorow">\n'
        for c in range(columns + int(r < rows_with_extra)):
            elem += '<div class="photocolumn"> {0} </div>\n'.format("{" + str(count) + "}")
            count += 1
        elem += '</div>\n'
    return elem

def get_album_block(album, photo_blocks):
    pre = """
<div class="album">
    <figure class="album">
""".format(album)
    #images = [x[0] for x in sorted(photo_blocks, key=order_photos)]
    images = [x[0] for x in photo_blocks]
    images_elem = get_grid(len(images)).format(*images)

    post = """
    <figcaption>
<?=$p->{0}->$lang;?> ~ <?=$p->{0}->year;?>
    </figcaption>
    </figure>
</div>
""".format(album)

    return pre + images_elem + post

def get_photo_captioned_figure(key, subdir, use_photo_caption = True, album_key = None):
    """
    Figure with caption.  If `album_key` is given AND `use_photo_caption` is True, 
    then we use the description from the album instead
    """
    image_key = album_key if album_key else key
    caption_year = " ~ <?=$p->{0}->year;?>".format(key)
    caption_key = key if use_photo_caption else album_key
    file_suffix = ".webp" if subdir == "lowres" else ""
    return """<figure class="image">
    <img src=<?="/photos/{2}/" . $p->{0}->name . "{4}";?> alt="<?=$p->{1}->$lang;?>{3}">
    <figcaption>
<?=$p->{1}->$lang;?>{3}
    </figcaption>
</figure>
""".format(key, caption_key, subdir, caption_year, file_suffix)

def get_photo_captioned_figure_with_previous_next(key, subdir, use_photo_caption = True, album_key = None, 
                                                  prev_file = None, next_file = None):
    """
    Figure with caption.  If `album_key` is given AND `use_photo_caption` is True, 
    then we use the description from the album instead
    """
    image_key = album_key if album_key else key
    caption_year = " ~ <?=$p->{0}->year;?>".format(key)
    caption_key = key if use_photo_caption else album_key
    file_suffix = ".webp" if subdir == "lowres" else ""
    return """<figure class="image">
    <img src=<?="/photos/{2}/" . $p->{0}->name . "{4}";?> alt="<?=$p->{1}->$lang;?>{3}">
    <figcaption>
    {5}
<?=$p->{1}->$lang;?>{3}
    {6}
    </figcaption>
</figure>
""".format(key, caption_key, subdir, caption_year, file_suffix,
    """<a class="prev_link" href="<?="./{0}.php";?>"><?=$language['Previous']?></a>""".format(prev_file) if prev_file else "",
    """<a class="next_link" href="<?="./{0}.php";?>"><?=$language['Next']?></a>""".format(next_file) if next_file else ""
           )

def get_photo_block(key, file_name):
    return """<a href="<?="/" . $lang . "/photos/{0}.php";?>">
{1}
</a>
""".format(file_name, get_photo_captioned_figure(key, "lowres"))

def get_photo_captioned_figure_in_album(key):
    return """<figure class="albumimage">
    <img class="albumimage" src=<?="/photos/lowres/" . $p->{0}->name . ".webp";?> alt="<?=$p->{0}->$lang;?>">
    <figcaption>
<?=$p->{0}->$lang;?>
    </figcaption>
</figure>
""".format(key)

def get_photo_block_in_album(key, file_name):
    return """<span style="color:grey"><a href="<?="/" . $lang . "/photos/{0}.php";?>">
{1}
</a></span>
""".format(file_name, get_photo_captioned_figure_in_album(key))

with open("photos.json", "r") as fw:
    photos = json.load(fw)
    album_photos = []
    for key,photo in photos.items():

        if "is_album" in photo and photo["is_album"]:
            album_photos += photo["photos"]

    photo_key_to_album_key = {}
    photo_key_to_previous = {}
    photo_key_to_next = {}
    for key,photo in photos.items():

        # ignore albums for now
        if key == "is_album":
            continue
        
        file_name = photo["name"].replace(".jpg","")

        if "is_album" in photo and photo["is_album"] == True:
            album_blocks = []
            for i,subkey in enumerate(photo["photos"]):
                photo_key_to_album_key[subkey] = key

                # Used to assign the 'Previous' and 'Next links on the single-photo page when the photo is part of an album
                photo_key_to_previous[subkey] = None if i == 0 else photo["photos"][i-1]
                photo_key_to_next[subkey] = None if i == len(photo["photos"]) - 1 else photo["photos"][i+1]

                sub_photo = photos[subkey]
                sub_file_name = sub_photo["name"].replace(".jpg","")
                sub_block = get_photo_block_in_album(subkey, sub_file_name)
                album_blocks.append((sub_block, sub_photo))
            block = get_album_block(key, album_blocks)
            photo_blocks.append((block, photo))


        # Photo is not contained in any album, so just print it on main photos page
        elif key not in album_photos:
            block = get_photo_block(key, file_name)
            photo_blocks.append((block, photo))
    
    print("\n\n".join([x[0] for x in sorted(photo_blocks, key=order_photos)]))
    
    # Get single-image pages (stored in raw_with_label)
    for key,photo in photos.items():
        # ignore albums for now
        if key == "is_album":
            continue
        
        file_name = photo["name"].replace(".jpg","")
        
        # The idea is that if the photo is (1) contained in an album and (2) doesn't have its own description,
        # then on the single-image page, we use the album caption rather than leaving it at "~ [year]"
        if key in photo_key_to_album_key:
            key_prev = photo_key_to_previous[key]
            key_next = photo_key_to_next[key]
            prev_file_name = photos[key_prev]["name"].replace(".jpg", "") if key_prev != None else None
            next_file_name = photos[key_next]["name"].replace(".jpg", "") if key_next != None else None
            block = get_photo_captioned_figure_with_previous_next(
            #block = get_photo_captioned_figure_with_previous_next(
            key, "raw", photo["en"] or photo["fr"], photo_key_to_album_key[key], prev_file_name, next_file_name)
        else:
            block = get_photo_captioned_figure(key, "raw")
        block = block.replace('class="image"', 'class="single-image"')
        
        html_path = "./raw_with_label/" + file_name + ".html"
        with open(html_path, "w") as f:
            f.write(block)
        for language in ["en", "fr"]:
            php_path = "../{0}/photos/{1}.php".format(language, file_name)
            with open(php_path, "w") as f:
                f.write("""<?php 
include($_SERVER['DOCUMENT_ROOT']."/photos/minimal_photo_header.php");
include($_SERVER['DOCUMENT_ROOT']."/{0}/minimal_header.html");
include($_SERVER['DOCUMENT_ROOT']."/photos/{1}");
?> 
""".format(language, html_path))
    
        



    

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
    #print(elem)
    return elem

def get_album_block(album, photo_blocks):
    pre = """
<div class="album">
    <figure class="album">
""".format(album)
    #images = [x[0] for x in sorted(photo_blocks, key=order_photos)]
    images = [x[0] for x in photo_blocks]
    images_elem = get_grid(len(images)).format(*images)

    #images_elem = "\n\n".join(images)
    post = """
    <figcaption>
<?=$p->{0}->$lang;?> ~ <?=$p->{0}->year;?>
    </figcaption>
    </figure>
</div>
""".format(album)

    return pre + images_elem + post

def get_photo_captioned_figure(key, subdir, year = True):
    return """<figure class="image">
    <img src=<?="/photos/{1}/" . $p->{0}->name;?>>
    <figcaption>
<?=$p->{0}->$lang;?>{2}
    </figcaption>
</figure>
""".format(key, subdir, " ~ <?=$p->{0}->year;?>".format(key) if year else "")

def get_photo_block(key, file_name, year = True):
    return """<a href="<?="/" . $lang . "/photos/{0}.php";?>">
{1}
</a>
""".format(file_name, get_photo_captioned_figure(key, "lowres", year))

def get_photo_captioned_figure_in_album(key):
    return """<figure class="albumimage">
    <img class="albumimage" src=<?="/photos/lowres/" . $p->{0}->name;?>>
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

    for key,photo in photos.items():

        # ignore albums for now
        if key == "is_album":
            continue
        
        file_name = photo["name"].replace(".jpg","")

        if "is_album" in photo and photo["is_album"] == True:
            album_blocks = []
            for subkey in photo["photos"]:
                subphoto = photos[subkey]
                sub_file_name = subphoto["name"].replace(".jpg","")
                block = get_photo_block_in_album(subkey, sub_file_name)
                album_blocks.append((block, subphoto))
            block = get_album_block(key, album_blocks)
            photo_blocks.append((block, photo))


        # Photo is not contained in any album, so just print it on main photos page
        elif key not in album_photos:
            block = get_photo_block(key, file_name)
            photo_blocks.append((block, photo))
        
        block = get_photo_captioned_figure(key, "raw").replace('class="image"', 'class="single-image"')
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
    
        

print("\n\n".join([x[0] for x in sorted(photo_blocks, key=order_photos)]))


    

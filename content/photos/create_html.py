import json
import os
import sys
from math import sqrt,floor
sys.path.append(os.path.abspath("../../"))
from helper import *

photo_blocks = []

# 2024.05

def get_grid(photo_count):
    rows = floor(sqrt(photo_count))
    columns = photo_count // rows
    rows_with_extra = photo_count % rows
    
    elem = """"""
    count = 0
    for r in range(rows):
        elem += '<div class="row">\n'
        for c in range(columns + int(r < rows_with_extra)):
            elem += '<div class="column"> {0} </div>\n'.format("{" + str(count) + "}")
            count += 1
        elem += '</div>\n'
    #print(elem)
    return elem
    
    
    

def get_album_block(album, photo_blocks):
    pre = """
<style>

/* Create two equal columns that sits next to each other */
.albumimage {
    width: auto;
    height: auto;
}
.album {
    display: grid;
    grid-auto-flow: column;
}

.row {
    display: flex;
    flex: 50%;
}
.column {
  padding: 1em;
}
</style>

<div class="album">
    <figure>
""".replace("{0}", album)
    images = [x[0] for x in sorted(photo_blocks, key=order_photos)]
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

def get_photo_block(key):
    return """<a href="<?="/photos/raw/" . $p->{0}->name;?>">
<figure class="image">
    <img src=<?="/photos/lowres/" . $p->{0}->name;?>>
    <figcaption>
<?=$p->{0}->$lang;?> ~ <?=$p->{0}->year;?>
    </figcaption>
    </figure>
</a>
""".format(key)

def get_photo_block_in_album(key):
    return """
<a href="<?="/photos/raw/" . $p->{0}->name;?>">
<img class="albumimage" src=<?="/photos/lowres/" . $p->{0}->name;?>>
</a>
""".format(key)

with open("photos.json", "r") as fw:
    photos = json.load(fw)
    album_photos = []
    for key,photo in photos.items():
        # ignore albums for now
        if "is_album" in photo and photo["is_album"]:
            album_photos += photo["photos"]
    for key,photo in photos.items():
        # ignore albums for now
        if key == "is_album":
            continue
        if "is_album" in photo and photo["is_album"] == True:
            album_blocks = []
            for subkey in photo["photos"]:
                subphoto = photos[subkey]
                # if subkey == "is_album":
                #     continue
                block = get_photo_block_in_album(subkey)
                album_blocks.append((block, subphoto))
            block = get_album_block(key, album_blocks)
            photo_blocks.append((block, photo))
            #print(block)
        elif key not in album_photos:
            block = get_photo_block(key)
            photo_blocks.append((block, photo))
        

print("\n\n".join([x[0] for x in sorted(photo_blocks, key=order_photos)]))


    

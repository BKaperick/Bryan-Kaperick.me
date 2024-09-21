import json
import os
import sys
sys.path.append(os.path.abspath("../../"))
from helper import *

photo_blocks = []

# 2024.05



def get_album_block(album, photo_blocks):
    pre = """<a href="<?="/photos/raw/" . $p->{0}->name;?>">
    <figure class="image">""".format(album)
    
    images_elem = "\n\n".join([x[0] for x in sorted(photo_blocks, key=order_photos)])
    
    post = """<figcaption>
<?=$p->{0}->$lang;?> ~ <?=$p->{0}->year;?>
    </figcaption>
    </figure>
</a>
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

with open("photos.json", "r") as fw:
    photos = json.load(fw)
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
                block = get_photo_block(subkey)
                album_blocks.append((block, subphoto))
            block = get_album_block(key, album_blocks)
            photo_blocks.append((block, photo))
            #print(block)
        else:
            block = get_photo_block(key)
            photo_blocks.append((block, photo))
        

print("\n\n".join([x[0] for x in sorted(photo_blocks, key=order_photos)]))


    

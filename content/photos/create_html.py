import json
import os
import sys
sys.path.append(os.path.abspath("../../"))
from helper import *

photo_blocks = []

# 2024.05



def get_album_block(album, photo_blocks):
    pre = """
<style>
.row {
  padding: 0 4px;
}

/* Create two equal columns that sits next to each other */
.albumimage {
    width: 300px;
    height: auto;
    max-width: 50%;
}
.album {
    display: grid;
    grid-auto-flow: column;
}

.column {
    width: 300px;
    display: flex;
  flex: 50%;
  padding: 0 4px;
}

.column img {
  margin-top: 8px;
  vertical-align: middle;
}
</style>

<div class="album">
    <a href="<?="/" . $lang . "/photos/" . $p->{0}->name . ".html"; ?>">
    <figure>
        <div class="row">
          <div class="column">
""".replace("{0}", album)
    images = [x[0] for x in sorted(photo_blocks, key=order_photos)]

    images_elem = """
    {0}
    {1}
    </div>
    <div class="column">
    {2}
    {3}
    """.format(*images)

    #images_elem = "\n\n".join(images)
    post = """
        </div>    
    </div>
</div>
    <figcaption>
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

def get_photo_block_in_album(key):
    return """<img class="albumimage" src=<?="/photos/lowres/" . $p->{0}->name;?>>
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


    

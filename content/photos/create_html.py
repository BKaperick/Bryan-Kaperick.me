import json
import os
import sys
sys.path.append(os.path.abspath("../../"))
from helper import *

photo_blocks = []

# 2024.05



with open("photos.json", "r") as fw:
    photos = json.load(fw)
    for key,photo in photos.items():
        
        # ignore albums for now
        if "is_album" in photo and photo["is_album"] == True:
            continue

        block = """<a href="<?="/photos/raw/" . $p->{0}->name;?>">
    <figure class="image">
    <img src=<?="/photos/lowres/" . $p->{0}->name;?>>
    <figcaption>
<?=$p->{0}->$lang;?> ~ <?=$p->{0}->year;?>
    </figcaption>
    </figure>
</a>
""".format(key)
        
        photo_blocks.append((block, photo))

print("\n\n".join([x[0] for x in sorted(photo_blocks, key=order_photos)]))


    

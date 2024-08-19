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
        block = """<figure class="image">
    <a href="<?="/content/photos/raw/" . $p->{0}->name;?>"><img src=<?="/content/photos/lowres/" . $p->{0}->name;?>>
    <figcaption>
<?=$p->{0}->$lang;?> ~ <?=$p->{0}->year;?>
    </figcaption>
    </a>
</figure>
""".format(key)
        
        photo_blocks.append((block, photo))

print("\n\n".join([x[0] for x in sorted(photo_blocks, key=order_photos)]))


    

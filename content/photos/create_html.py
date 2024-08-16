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
    <img src=<?="/content/" . $p->{0}->rawpath;?>>
    <figcaption>
<?=$p->{0}->$language;?> ~ <?=$p->{0}->year;?>
    </figcaption>
</figure>
""".format(key)
        
        photo_blocks.append((block, photo))

print("\n\n".join([x[0] for x in sorted(photo_blocks, key=order_photos)]))


    

import json
import os
import sys
sys.path.append(os.path.abspath("../../"))
from helper import *

now_blocks = []

# 2024.05



with open("now.json", "r") as fw:
    nows = json.load(fw)
    for key,now in nows.items():
        block = """<a href="<?="/content/nows/raw/" . $p->{0}->photo;?>">
    <figure class="image">
    <img src=<?="/content/nows/raw/" . $p->{0}->photo;?>>
    <figcaption>
<?=$p->{0}->$lang;?> ~ <?=$p->{0}->date;?>
    </figcaption>
    </figure>
</a>
""".format(key)
        
        now_blocks.append((block, now))

print("\n\n".join([x[0] for x in sorted(now_blocks)]))


    

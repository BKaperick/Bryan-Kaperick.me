import os
import sys
sys.path.append(os.path.abspath("../../"))
from helper import *
import json
attribution_blocks = []

def get_block(key):
    return """
<li>
    <a id="american" href="<?= $p->{0}->link?>">
        <img src="<?=$p->{0}->image;?>" class="invertible">
        <?=$p->{0}->name;?> by <?=$p->{0}->author;?></a> is licensed under <a href="<?= $p->{0}->license_link?>"><?=$p->{0}->license;?></a>
</li>
""".format(key)

blocks = []
with open("attributions.json", "r") as fr:
    attrs = json.load(fr)
    for key in attrs.keys():
        blocks.append(get_block(key))

with open("attributions.html", "w") as fw:
    fw.write("\n\n".join(blocks))

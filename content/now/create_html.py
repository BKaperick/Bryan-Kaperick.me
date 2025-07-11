import json
import os
import sys
sys.path.append(os.path.abspath("../../"))
from helper import *

now_blocks = []

# 2024.05
#caption {
#  border: 1px solid #eeeeee;
#}

header = """
<table class="bordered" border=1 frame=sides cellspacing="0" cellpadding="5">
  <tr>
    <th class="border1">Location</th>
    <th class="border1">Date</th>
    <th class="border1">Update</th>
    <th class="border1">Photo</th>
  </tr>

"""
 #
footer = """
</table>
"""

with open("now.json", "r") as fw:
    nows = json.load(fw)
    for key,now in nows.items():
        block = """
<tr> 
    <td><?=$p->{0}->location;?></td>
    <td class="border1" style="min-width:100px"><?=$p->{0}->date;?></td>
    <td class="border1"><?=$p->{0}->$lang;?></td>
    <td class="border1"><a href="<?="/now/raw/" . $p->{0}->photo;?>">
        <img src="<?="/now/lowres/" . $p->{0}->photo . ".webp";?>" style="max-width:60px;width:100%"></a></td>
</tr>
""".format(key)
        
        now_blocks.append((block, now))
sorted_blocks = sorted(now_blocks, key=lambda x : x[1]['date'], reverse=True)
date = str(sorted_blocks[0][1]['date']) + "</p>\n\n"
print(date + header + "\n\n".join([x[0] for x in sorted_blocks]) + footer)


    

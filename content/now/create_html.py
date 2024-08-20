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
<style>
.border1 {
  border-top:thin solid;
  border-bottom:thin solid;
  border-left:thin solid;
  border-right:thin solid;
  border-color:black;
  padding: 5px;
}
table {
  border: 2px solid black;
}
td {
  text-align: center;
  vertical-align: middle;
}
</style>

<table border=1 frame=sides cellspacing="0" cellpadding="5">
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
        <img src="<?="/now/lowres/" . $p->{0}->photo;?>" style="max-width:60px;width:100%"></a></td>
</tr>
""".format(key)
        
        now_blocks.append((block, now))

print(header + "\n\n".join([x[0] for x in sorted(now_blocks, key=lambda x : x[1]['date'], reverse=True)]) + footer)


    

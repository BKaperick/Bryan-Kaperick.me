import os
import sys
from datetime import datetime
import json

with open('argot_content.html', 'w') as fw:
    with open('argot.txt', 'r') as fr:
        content = fr.read()
        content = content.replace("*", "<em>", 1)
        content = content.replace("*", "</em>", 1)
        content = content.replace("--", "&ndash;", 1)
        fw.write(content)
        # *se capitonner* -- Garnir le corsage de sa robe d'avantages en coton pour séduire les hommes

with open('datapoint_content.html', 'w') as fw:
    with open('datapoint.txt', 'r') as fr:
        content = fr.read()
        content = content.replace("*", "<em>", 1)
        content = content.replace("*", "</em>", 1)
        fw.write(content)
        # In Egypt in 2009, the *neonatal mortality rate (deaths per 1,000 live births)* was 16.0


def latest_updates_from_content(lang):
    out = ["<ul>"]
    with open('../scripts/content_{0}.json'.format(lang), 'r+') as fr:
        content = [p for p in json.load(fr)][:3]
        for c in content:
            date = datetime.strptime(c["date"], "%Y%m%d")
            month = date.strftime("%b")
            translated_date = date.strftime("M %Y").replace("M", "<?php echo $language['{0}'] ?>".format(month)) 
            #translated_date = translated_date[1:] if translated_date[0] == "0" else translated_date
            out.append("""<li>{0}: <?php echo $language['new-{1}'] ?> &ndash; <a href="{3}">{2}</a></li>""".format(translated_date, c["category"], c["desc"], c["link"]))
    out.append("</ul>")
    return "\n".join(out)

for lang in ["en", "fr"]:
    with open('latest_updates_content_{0}.html'.format(lang), 'w') as fw:
        fw.write(latest_updates_from_content(lang))

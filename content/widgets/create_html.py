import os
import sys
from datetime import datetime
import json

with open('argot_content.html', 'w') as fw:
    with open('argot.json', 'r') as fr:
        content = json.load(fr)
        print(content)
        term_and_year = f"<em>{content['term']}" + "" if content['year'] == None else f" ({content['year']})"
        out_str = f"{term_and_year}</em> &ndash; {content['definition']}"
        fw.write(out_str)
        # *se capitonner* -- Garnir le corsage de sa robe d'avantages en coton pour séduire les hommes
        # <em>nougat</em> &ndash; Argent, butin ; place, situation qui rapporte de l'argent

with open('datapoint_content.html', 'w') as fw:
    with open('datapoint.txt', 'r') as fr:
        content = fr.read()
        content = content.replace("*", "<em>", 1)
        content = content.replace("*", "</em>", 1)
        fw.write(content)
        # In Egypt in 2009, the *neonatal mortality rate (deaths per 1,000 live births)* was 16.0


def latest_updates_from_content(lang):
    #out = ["<ul>"]
    out = ['<table class="no-border>"']
    with open('../scripts/content_{0}.json'.format(lang), 'r+') as fr:
        content = [p for p in json.load(fr)][:3]
        for c in content:
            date = datetime.strptime(c["date"], "%Y%m%d")
            month = date.strftime("%b")
            translated_date = date.strftime("M %Y").replace("M", "<?php echo $language['{0}'] ?>".format(month)) 
            #out.append("""<li>{0}: <?php echo $language['new-{1}'] ?> &ndash; <a href="{3}">{2}</a></li>""".format(translated_date, c["category"], c["title"], c["link"]))
            precise_category_type = "new-" + c["category"]
            if "is_album" in c and c["is_album"]:
                precise_category_type += "-album"
            print(precise_category_type)
            out.append("""<tr>
            <td class="latest-updates">{0}</td>
            <td class="latest-updates"><?php echo $language['{1}'] ?></td>
            <td class="latest-updates"><a href="{3}">{2}</a></td>\n</tr>
                       """.format(translated_date, precise_category_type, c["title"], c["link"]))
    #out.append("</ul>")
    out.append("</table>")
    return "\n".join(out)

for lang in ["en", "fr"]:
    with open('latest_updates_content_{0}.html'.format(lang), 'w') as fw:
        fw.write(latest_updates_from_content(lang))

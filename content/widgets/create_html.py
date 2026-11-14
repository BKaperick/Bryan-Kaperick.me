import json
from datetime import datetime

with open("argot_content.html", "w") as fw, open("argot.json", "r") as fr:
    content = json.load(fr)
    term_and_year = (
        f"{content['term']}" + ""
        if content["year"] == None
        else f" ({content['year']})"
    )
    out_str = f"<em>{term_and_year}</em> &ndash; {content['definition']}"
    fw.write(out_str)
    # *se capitonner* -- Garnir le corsage de sa robe d'avantages en coton pour séduire les hommes

with open("datapoint_content.html", "w") as fw, open("datapoint.txt", "r") as fr:
    content = fr.read()
    content = content.replace("*", "<em>", 1)
    content = content.replace("*", "</em>", 1)
    fw.write(content)
    # In Egypt in 2009, the *neonatal mortality rate (deaths per 1,000 live births)* was 16.0


def latest_updates_from_content(lang):
    # out = ["<ul>"]
    out = ['<table class="no-border>"']
    with open(f"../scripts/content_{lang}.json", "r+") as fr:
        content = [p for p in json.load(fr)][:3]
        for c in content:
            date = datetime.strptime(c["date"], "%Y%m%d")
            month = date.strftime("%b")
            translated_date = date.strftime("M %Y").replace(
                "M", f"<?php echo $language['{month}'] ?>"
            )
            # out.append("""<li>{0}: <?php echo $language['new-{1}'] ?> &ndash; <a href="{3}">{2}</a></li>""".format(translated_date, c["category"], c["title"], c["link"]))
            precise_category_type = "new-" + c["category"]
            if c.get("is_album"):
                precise_category_type += "-album"
            print(precise_category_type)
            out.append(f"""<tr>
            <td class="latest-updates">{translated_date}</td>
            <td class="latest-updates"><?php echo $language['{precise_category_type}'] ?></td>
            <td class="latest-updates"><a href="{c["link"]}">{c["title"]}</a></td>\n</tr>
                       """)
    # out.append("</ul>")
    out.append("</table>")
    return "\n".join(out)


for lang in ["en", "fr"]:
    with open(f"latest_updates_content_{lang}.generated.html", "w") as fw:
        fw.write(latest_updates_from_content(lang))

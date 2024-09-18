import sys
import json

target = []
format_all = False
if len(sys.argv) > 1:
    if sys.argv[1] == 'all-poems':
        format_all = True
    else:
        target = " ".join(sys.argv[1:])

def format_poem(poem):
    out = []
    for line in poem:
        out.append(format_line(line))
    for i,l in enumerate(out):
        if i > 0 and l == "</p>\n<p><span class=\"line\">":
            out[i-1] = out[i-1].replace("<br>", "").replace("\n","")
    out[-1] = out[-1].replace("</span><br>\n", "")
    poem_body = "<div class=\"poem\"><p>" + "".join(out) + r"</p></div>"
    return poem_body


def format_line(line):
    line = line.rstrip()
    if not line:
        return "</p></div>\n<div class=\"poem\"><p>"
    line = line.replace("    ", "&nbsp;&nbsp;&nbsp;")
    line = line.replace("--", "&mdash;")
    return "<span class=\"line\">" + line + "</span><br>\n"

with open("poems.json", 'r+') as fwrite:
    poems = json.load(fwrite)
    for name, poem_metadata in poems.items():
        if (format_all and 'rawpath' in poem_metadata) or (not "body" in poem_metadata) or (name in target):
            print("Auto-formatting \"" + poem_metadata['title'] + "\" from " + poem_metadata['rawpath'])
            with open(poem_metadata['rawpath'], 'r') as fin:
                poem_body = format_poem(list(fin.readlines()))
                poems[name]['body'] = poem_body

    fwrite.seek(0)
    json.dump(poems, fwrite, indent=4)
    fwrite.truncate()

    
        



import sys
import json

target = []
format_all = False
if len(sys.argv) > 1:
    if sys.argv[1] == "all-posts":
        format_all = True
    else:
        target = " ".join(sys.argv[1:])


def format_italics(text: str):
    new_text = text
    second_new_text = ""
    while new_text != second_new_text:
        second_new_text = new_text
        new_text = new_text.replace("*", "<i>", 1)
        new_text = new_text.replace("*", "</i>", 1)
    return new_text


def format_post(post):
    out = []
    for line in post:
        out.append(format_line(line))
    for i, l in enumerate(out):
        if i > 0 and l == '</p>\n<p><span class="line">':
            out[i - 1] = out[i - 1].replace("<br>", "").replace("\n", "")
    out[-1] = out[-1].replace("</span><br>\n", "")
    post_body = '<div class="post"><p>' + "".join(out) + r"</p></div>"

    new_post_body = post_body
    second_new_post_body = ""
    while new_post_body != second_new_post_body:
        second_new_post_body = new_post_body
        new_post_body = new_post_body.replace("*", "<i>", 1)
        new_post_body = new_post_body.replace("*", "</i>", 1)
    return new_post_body


def format_line(line):
    line = line.rstrip()
    if not line:
        return '</p></div>\n<div class="post"><p>'
    line = line.replace("    ", "&nbsp;&nbsp;&nbsp;")
    line = line.replace("--", "&mdash;")
    return line  # '<span class="line">' + line + "</span><br>\n"


with open("posts.json", "r+") as fwrite:
    posts = json.load(fwrite)
    for name, post_metadata in posts.items():
        if (
            (format_all and "rawpath" in post_metadata)
            or ("body" not in post_metadata)
            or (name in target)
        ):
            print(
                'Auto-formatting "'
                + post_metadata["title"]
                + '" from '
                + post_metadata["rawpath"]
            )
            with open(post_metadata["rawpath"], "r") as fin:
                raw_lines = list(fin.readlines()[1:])
                post_body = format_post(raw_lines)
                posts[name]["body"] = post_body
                # raw_body is fed to the search index, so we don't want html formatting.
                posts[name]["raw_body"] = " ".join([l.strip() for l in raw_lines])

    fwrite.seek(0)
    json.dump(posts, fwrite, indent=4)
    fwrite.truncate()

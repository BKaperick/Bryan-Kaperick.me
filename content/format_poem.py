import sys

# python format_poem.py input.txt output.md
fname = sys.argv[1]
fname_out = sys.argv[2]

def format_line(line):
    line = ">" + line.strip() + "  \n"
    line = line.replace("    ", "&nbsp;&nbsp;&nbsp;")
    line = line.replace("--", "&mdash;")
    return line

with open(fname_out, 'w') as fout:
    with open(fname, 'r') as fin:
        for line in fin.readlines():
            formatted_line = format_line(line)
            fout.write(formatted_line)




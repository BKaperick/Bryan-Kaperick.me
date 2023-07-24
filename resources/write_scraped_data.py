import re
import os
file_regex = re.compile('www\.languefrancaise\.net-.*\.txt')

def pop_from_file(fname):
    lines = open(fname).readlines()
    if not lines:
        os.remove(fname)
        return None
    line = lines[0]
    del lines[0]
    open(fname, 'w').writelines(lines)
    return line

if __name__ == '__main__':
    for f in os.listdir():

        if file_regex.match(f):
            data = pop_from_file(f)
            print(data)

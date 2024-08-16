import os
import sys

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

cd ./content/poems
python3 instantiate.py
python3 format_poem.py
python3 create_html.py
cd ../photos
python3 instantiate.py
python3 create_html.py > photos.html
cd ../widgets
python3 create_html.py
cd ../..

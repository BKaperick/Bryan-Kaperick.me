cd ./content/poems
python instantiate.py
python format_poem.py
python create_html.py
cd ../photos
python instantiate.py
python create_html.py > photos.html
cd ../..

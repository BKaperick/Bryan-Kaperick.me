#!/bin/bash

echo $PATH

cd ./content/poems
echo "starting poetry ingestion"
/__t/Python/3.13.9/x64/bin/python ./scripts/instantiate.py
python ./scripts/format_poem.py all-poems
python ./scripts/create_html.py

cd ../now
echo "starting now ingestion"
python instantiate.py "$1"
../../compress.sh
python create_html.py > now.html

cd ../photos
echo "starting photo ingestion"
python instantiate.py "$1"
../../compress.sh
python create_html.py > photos.html

cd ../widgets
echo "starting widget ingestion"
./update_last_update.sh
python create_html.py

cd ../attributions
echo "starting attributions ingestion"
python create_html.py

cd ../projects
echo "starting project ingestion"
python ./scripts/create_html.py

cd ../bio
echo "starting bio page ingestion"
python ./scripts/create_html.py
python ./scripts/ingest_films.py films.json
python ./scripts/create_movie_html.py

cd ../scripts
echo "starting rss feed content creation"
python ./create_rss.py

cd ../..
echo "finished data ingestion"

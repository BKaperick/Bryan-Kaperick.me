#!/bin/bash

cd ./content/poems
echo "starting poetry ingestion"
python3 ./scripts/instantiate.py
python3 ./scripts/format_poem.py all-poems
python3 ./scripts/create_html.py

cd ../now
echo "starting now ingestion"
if [[ "$1" == "draft" ]]; then
    python3 instantiate.py ""
else
    python3 instantiate.py "$1"
fi

../../compress.sh
python3 create_html.py > now.generated.html

cd ../photos
echo "starting photo ingestion"
if [[ "$1" == "draft" ]]; then
    python3 instantiate.py ""
else
    python3 instantiate.py "$1"
fi
../../compress.sh
python3 create_html.py > photos.generated.html

cd ../widgets
echo "starting widget ingestion"
if [[ "$1" == "draft" ]]; then
    echo "Skipping last_update in draft mode."
else
    ./update_last_update.sh
fi
python3 create_html.py

cd ../attributions
echo "starting attributions ingestion"
python3 create_html.py

cd ../projects
echo "starting project ingestion"
python3 ./scripts/create_html.py

cd ../bio
echo "starting bio page ingestion"
python3 ./scripts/create_html.py
python3 ./scripts/ingest_films.py films.json
python3 ./scripts/create_movie_html.py

cd ../../resources

if [[ "$1" == "draft" ]]; then
    echo "Skipping slang scraping in draft mode."
else
    # python3 ./datagetter.py ../content/widgets/datapoint.txt
    python3 ./write_scraped_data.py ../content/widgets argot.json
fi

cd ../content/scripts
echo "starting rss feed content creation"
python3 ./create_rss.py

cd ../..
echo "finished data ingestion"

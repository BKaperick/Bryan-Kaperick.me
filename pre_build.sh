cd ./content/poems
echo "starting poetry ingestion"
./pre_build.sh
python3 ./scripts/instantiate.py
python3 ./scripts/format_poem.py
python3 ./scripts/create_html.py

cd ../now
echo "starting now ingestion"
python3 instantiate.py "$1"
../../compress.sh
python3 create_html.py > now.html

cd ../photos
echo "starting photo ingestion"
python3 instantiate.py "$1"
../../compress.sh
python3 create_html.py > photos.html

cd ../widgets
echo "starting widget ingestion"
python3 create_html.py

cd ../attributions
echo "starting attributions ingestion"
python3 create_html.py

cd ../..
echo "finished data ingestion"

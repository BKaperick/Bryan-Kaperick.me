cd ./content/poems
echo "starting poetry ingestion"
python3 instantiate.py
python3 format_poem.py
python3 create_html.py
cd ../now
echo "starting now ingestion"
python3 instantiate.py "$1"
../../compress.sh
python3 create_html.py > nows.html
cd ../photos
echo "starting photo ingestion"
python3 instantiate.py "$1"
../../compress.sh
python3 create_html.py > photos.html
cd ../widgets
echo "starting widget ingestion"
python3 create_html.py
cd ../..
echo "finished data ingestion"

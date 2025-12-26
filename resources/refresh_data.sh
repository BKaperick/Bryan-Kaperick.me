#!/bin/bash
DIR="$( cd "$( dirname "$0" )" && pwd )"
source ~/website-env/bin/activate
python $DIR/../content/bio/scripts/ingest_films.py $DIR/../content/bio/films.json
python $DIR/datagetter.py $DIR/../content/widgets/datapoint.txt
python $DIR/write_scraped_data.py $DIR/../content/widgets/argot.json
echo "$DIR"
git -C /home/bryan/Bryan-Kaperick.me pull origin --ff-only
git -C /home/bryan/Bryan-Kaperick.me add "$DIR/../content/widgets/datapoint.txt"
git -C /home/bryan/Bryan-Kaperick.me add "www*"
git -C /home/bryan/Bryan-Kaperick.me add "$DIR/../content/widgets/argot.json"
git -C /home/bryan/Bryan-Kaperick.me commit -m "Update data point"
git -C /home/bryan/Bryan-Kaperick.me add "$DIR/../content/bio/films.json"
git -C /home/bryan/Bryan-Kaperick.me diff-index --quiet HEAD || git -C /home/bryan/Bryan-Kaperick.me commit -m "Update films"
git -C /home/bryan/Bryan-Kaperick.me push

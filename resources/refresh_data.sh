#!/bin/bash
DIR="$( cd "$( dirname "$0" )" && pwd )"
source $DIR/../.venv/bin/activate
python $DIR/../content/bio/scripts/ingest_films.py $DIR/../content/bio/films.json
# python $DIR/datagetter.py $DIR/../content/widgets/datapoint.txt
python $DIR/write_scraped_data.py $DIR/../content/widgets/argot.json
echo "$DIR"
git -C $DIR/.. pull origin --ff-only
git -C $DIR/.. add "$DIR/../content/widgets/datapoint.txt"
git -C $DIR/.. add "www*"
git -C $DIR/.. add "$DIR/../content/widgets/argot.json"
git -C $DIR/.. commit -m "Update data point"
git -C $DIR/.. add "$DIR/../content/bio/films.json"
git -C $DIR/.. diff-index --quiet HEAD || git -C $DIR/.. commit -m "Update films"
git -C $DIR/.. push

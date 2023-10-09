#!/bin/bash
DIR="$( cd "$( dirname "$0" )" && pwd )"
python $DIR/datagetter.py $DIR/../content/datapoint.txt
python $DIR/write_scraped_data.py $DIR/../content/argot.txt
echo "$DIR"
git -C /home/bryan/Bryan-Kaperick.me pull origin --ff-only
git -C /home/bryan/Bryan-Kaperick.me add "$DIR/../content/datapoint.txt"
git -C /home/bryan/Bryan-Kaperick.me add "$DIR/../content/argot.txt"
git -C /home/bryan/Bryan-Kaperick.me commit -m "Update data point"
git -C /home/bryan/Bryan-Kaperick.me push

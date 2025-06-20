#!/bin/bash
DIR="$( cd "$( dirname "$0" )" && pwd )"
source ~/website-env/bin/activate
python $DIR/datagetter.py $DIR/../content/widgets/datapoint.txt
python $DIR/write_scraped_data.py $DIR/../content/widgets/argot.txt
echo "$DIR"
git -C /home/bryan/Bryan-Kaperick.me pull origin --ff-only
git -C /home/bryan/Bryan-Kaperick.me add "$DIR/../content/widgets/datapoint.txt"
git -C /home/bryan/Bryan-Kaperick.me add "www*"
git -C /home/bryan/Bryan-Kaperick.me add "$DIR/../content/widgets/argot.txt"
git -C /home/bryan/Bryan-Kaperick.me commit -m "Update data point"
git -C /home/bryan/Bryan-Kaperick.me push

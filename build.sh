pkill -f php
(php -S localhost:8000 -t content/) &
sleep $1s
rm -rf public
mkdir public
cd public
wget -q -k -K  -E -r -l 10 -p -N -F -nH localhost:8000
cd ..
./cleanup.sh

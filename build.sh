cd content
(php -S localhost:8000) &
cd ..
rm -r public
mkdir public
cd public
wget -k -K  -E -r -l 10 -p -N -F -nH http://localhost:8000
pkill -f php
cd ..
pwd
./cleanup.sh

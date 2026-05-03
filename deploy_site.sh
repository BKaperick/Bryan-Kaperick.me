pkill -f php
cd public
php -S 127.0.0.1:8000 &
cd ../content
php -S 127.0.0.1:8001 &
#php -S 127.0.0.1:8000 > /dev/null 2>&1 &
cd ..

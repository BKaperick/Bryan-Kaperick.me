cd raw
for file in $( find . -size -$((800*800))c )
do
    if ! test -f "../lowres/$file.webp"; then
        # TODO when ubuntu supports magick (updated version of convert) we can use this commented
        # line, but for now gh actions is on an ubuntu container
        #magick $file -strip -interlace Plane -gaussian-blur 0.05 -quality 85% "../lowres/$file"
        #convert -strip -interlace Plane -gaussian-blur 0.05 -quality 50% $file  "../lowres/$file"
        convert $file -quality 50% "../lowres/$file.webp" 
    fi
done
for file in $( find . -size +$((800*800))c )
do
    if ! test -f "../lowres/$file.webp"; then
        echo "Large file: $file"
        # TODO when ubuntu supports magick (updated version of convert) we can use this commented
        # line, but for now gh actions is on an ubuntu container
        #magick $file -strip -interlace Plane -gaussian-blur 0.05 -quality 85% "../lowres/$file"
        #convert -strip -interlace Plane -gaussian-blur 0.05 -quality 10% $file  "../lowres/$file"
        convert $file -quality 10% "../lowres/$file.webp" 
    fi
done
cd ..

# find . -type f -wholename "./raw/*" -exec convert -strip -interlace Plane -gaussian-blur 0.05 -quality 85% source.jpg result.jpg {} \;

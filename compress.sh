cd raw
for file in ./*
do
    if ! test -f "../lowres/$file"; then
        # TODO when ubuntu supports magick (updated version of convert) we can use this commented
        # line, but for now gh actions is on an ubuntu container
        #magick $file -strip -interlace Plane -gaussian-blur 0.05 -quality 85% "../lowres/$file"
        convert -strip -interlace Plane -gaussian-blur 0.05 -quality 75% $file  "../lowres/$file"
    fi
done
for file in $( find . -size +1M )
do
    if ! test -f "../lowres/$file"; then
        echo "Large file: $file"
        # TODO when ubuntu supports magick (updated version of convert) we can use this commented
        # line, but for now gh actions is on an ubuntu container
        #magick $file -strip -interlace Plane -gaussian-blur 0.05 -quality 85% "../lowres/$file"
        convert -strip -interlace Plane -gaussian-blur 0.05 -quality 25% $file  "../lowres/$file"
    fi
done
cd ..

# find . -type f -wholename "./raw/*" -exec convert -strip -interlace Plane -gaussian-blur 0.05 -quality 85% source.jpg result.jpg {} \;

cd raw
for file in ./*
do
    # TODO when ubuntu supports magick (updated version of convert) we can use this commented
    # line, but for now gh actions is on an ubuntu container
    #magick $file -strip -interlace Plane -gaussian-blur 0.05 -quality 85% "../lowres/$file"
    convert -strip -interlace Plane -gaussian-blur 0.05 -quality 75% $file  "../lowres/$file"
done
for file in $( find . -size +1M )
do
    echo "Large file: $file"
    # TODO when ubuntu supports magick (updated version of convert) we can use this commented
    # line, but for now gh actions is on an ubuntu container
    #magick $file -strip -interlace Plane -gaussian-blur 0.05 -quality 85% "../lowres/$file"
    convert -strip -interlace Plane -gaussian-blur 0.05 -quality 25% $file  "../lowres/$file"
done
cd ..

# find . -type f -wholename "./raw/*" -exec convert -strip -interlace Plane -gaussian-blur 0.05 -quality 85% source.jpg result.jpg {} \;
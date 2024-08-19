cd raw
for file in ./*
do
    echo $file
    # magick -strip -interlace Plane -gaussian-blur 0.05 -quality 85% file 
    magick $file -strip -interlace Plane -gaussian-blur 0.05 -quality 85% "../lowres/$file"
done
cd ..

# find . -type f -wholename "./raw/*" -exec convert -strip -interlace Plane -gaussian-blur 0.05 -quality 85% source.jpg result.jpg {} \;

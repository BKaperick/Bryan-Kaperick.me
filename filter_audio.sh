for f in $( find ../raw_audios -type f); do
    newname=`echo "$f" | sed 's/raw_audios/bryankaperickme\/content\/poems\/recordings/'`

    if ! test -f $newname; then
        ffmpeg -i $f -af "highpass=f=200, lowpass=f=3000" $newname 
        echo "current file is $f -> $newname"
    fi
    #mv "$f" "$newname"
done

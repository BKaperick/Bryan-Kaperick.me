for f in $( find ../raw_audios); do
    newname=`echo "$f" | sed 's/raw_audios/bryankaperickme\/content\/poems\/recordings/'`
    ffmpeg -i $f -af "highpass=f=200, lowpass=f=3000" $newname 
    echo "current file is $f -> $newname"
    #mv "$f" "$newname"
done

for i in $(seq 160);do
    #echo $i
    name=ShackHartmannsubapLocation_led$i.fits 
    if [ -f $name ];then
        sufix=${name##*_}
        newname=SHsubapLocation_$sufix
#        echo $newname
#        echo "mv $name $newname"
        mv $name $newname
    fi
done

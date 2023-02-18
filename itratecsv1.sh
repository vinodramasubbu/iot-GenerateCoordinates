cat nycoordinates1.csv | while read line 
do
   #echo $line|awk -F',' '{print $1}'
   slat=`echo $line|awk -F',' '{print $1}'`
   slon=`echo $line|awk -F',' '{print $2}'`
   dlat=`echo $line|awk -F',' '{print $3}'`
   dlon=`echo $line|awk -F',' '{print $4}'`
   #echo $line|awk -F',' '{print $1}'
   #echo $line|awk -F',' '{print $2}'
   #echo $line|awk -F',' '{print $3}'
   #echo $line|awk -F',' '{print $4}`
   #echo ${slat}

   echo "\""origin"\":" "\""${slat}","${slon}"\""","
   echo "\""destination"\":" "\""${dlat}","${dlon}"\""","
done

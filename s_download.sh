#!/bin/bash

if [ "$1" = 2019 ]
then 
    days=365
else
    days=366
fi

for (( i=1; i <= $days; ++i ))
do
    theday=`printf %03d $i` #the number of days in the year
    wget -r -l1 -nd -nc -np -e robots=off -A.nc --no-check-certificate https://www.star.nesdis.noaa.gov/thredds/fileServer/SMAP/daily/${1}/SP_D${1}${theday}_Map_SATSSS_data_1day.nc
done
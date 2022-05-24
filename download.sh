#!/bin/bash
init_date=`printf "$1""0""$2""01"` # pass command line arguments
startdate=$( gdate -d "$init_date" +'%Y%m01' )
enddate=$( gdate -d "$startdate +1 month - 1 day" +'%Y%m%d' )

thedate=$startdate

while [ "$thedate" != "$enddate" ]; do
  themonth=$( gdate -d "$thedate" +%Y%m )
  wget -r -l1 -nd -nc -np -e robots=off -A.nc --no-check-certificate https://www.ncei.noaa.gov/thredds/fileServer/OisstBase/NetCDF/V2.1/AVHRR/${themonth}/oisst-avhrr-v02r01.${thedate}.nc
  thedate=$( gdate -d "$thedate + 1 days" +%Y%m%d ) # increment by one day
done
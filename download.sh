#!/bin/bash

startdate='2019-01-01' # specify the date you want to start and end for the files
enddate='2019-02-28'

enddate=$( gdate -d "$enddate + 1 day" +%Y%m%d )
thedate=$( gdate -d "$startdate" +%Y%m%d )

while [ "$thedate" != "$enddate" ]; do
  themonth=$( gdate -d "$thedate" +%Y%m )
  wget -r -l1 -nd -nc -np -e robots=off -A.nc --no-check-certificate https://www.ncei.noaa.gov/thredds/fileServer/OisstBase/NetCDF/V2.1/AVHRR/${themonth}/oisst-avhrr-v02r01.${thedate}.nc
  thedate=$( gdate -d "$thedate + 1 days" +%Y%m%d ) # increment by one day
done
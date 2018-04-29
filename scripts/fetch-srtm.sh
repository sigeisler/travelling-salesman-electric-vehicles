#!/bin/bash

URL=${1}
MIN_LON=${2}
MAX_LON=$((${3}-1))
MIN_LAT=${4}
MAX_LAT=$((${5}-1))
DIR=${6}

for lon in $( seq ${MIN_LON} ${MAX_LON} ) ; 
do
    for lat in  $( seq ${MIN_LAT} ${MAX_LAT} ) ; 
    do
        file="N"$(printf '%02d' "${lon}")"E"$(printf '%03d' "${lat}")".hgt"
        tile_url=${URL}${file}".zip"
        if [ -f ${DIR}/${file}* ]
        then
            echo "tile '${file}' exists'"
        else
            echo "get tile from '${tile_url}'"
            wget -P ${DIR} ${tile_url}
        fi
    done
done

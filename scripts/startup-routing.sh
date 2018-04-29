#!/bin/bash

OSM_FILE=${1}
OSRM_FOLDER=${2}
OSRM_PROFILE=${3}
PORT=${4}

docker run -t --link elevation_postgis \
    -v $(pwd)/${OSRM_FOLDER}/${OSRM_PROFILE}/:/data \
    osrm/osrm-backend osrm-extract \
    -p /data/${OSRM_PROFILE}.lua \
    /data/${OSM_FILE}.osm.pbf
docker run -t -v $(pwd)/${OSRM_FOLDER}/${OSRM_PROFILE}/:/data \
    osrm/osrm-backend osrm-partition /data/${OSM_FILE}.osrm
docker run -t -v $(pwd)/${OSRM_FOLDER}/${OSRM_PROFILE}/:/data \
    osrm/osrm-backend osrm-customize /data/${OSM_FILE}.osrm
docker run -d -t -i -p ${PORT}:5000 \
        -v $(pwd)/${OSRM_FOLDER}/${OSRM_PROFILE}/:/data \
        osrm/osrm-backend osrm-routed \
        --algorithm mld \
        /data/${OSM_FILE}.osrm
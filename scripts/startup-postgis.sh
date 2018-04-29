#!/bin/bash

POSTGRES_PW=${1}
DATA_FOLDER=${2}

! docker ps | grep -q elevation_postgis && \
    (docker run --rm --name elevation_postgis \
        -e POSTGRES_PASSWORD=${POSTGRES_PW} \
        -p 5432:5432 \
        -v $(pwd)/${DATA_FOLDER}:/${DATA_FOLDER} \
        -d \
        mdillon/postgis || \
    docker start elevation_postgis)

exit 0

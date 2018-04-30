#!/bin/bash

OSM_URL=${1}
OSM_FILE=${2}

[ ! -f osrm/${OSM_FILE}.osm.pbf ] && wget -P osrm ${OSM_URL}${OSM_FILE}.osm.pbf
#!/bin/bash
DIR=${1}

for f in ${DIR}/*.hgt.zip;
do 
    if [ -f "${f}" ] 
    then
        echo "unzip tile: ${f}";
        unzip ${f} -d ${DIR}; 
        rm ${f}
    fi
done;

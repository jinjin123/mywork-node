#!/bin/bash

#Enable section
CC=0
CRM=1
MKT=1
DE=1
PMT=1
FE=1

if [ ! -z ${CC} ] && [ ${CC} -eq 1 ];
then
    echo "RUN!"
fi

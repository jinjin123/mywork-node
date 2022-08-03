#!/bin/bash
IP=(182.92.213.195 203.195.217.192 14.152.80.145 202.104.174.113)
length=${#IP[@]}
printf "{\n"
printf  '\t'"\"data\":["
for ((i=0;i<$length;i++))
do
        printf '\n\t\t{'
        printf "\"{#IP_ADDR}\":\"${IP[$i]}\"}"
        if [ $i -lt $[$length-1] ];then
                printf ','
        fi
done
printf  "\n\t]\n"
printf "}\n"


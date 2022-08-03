#!/bin/bash
IP=(118.194.37.2 118.194.37.3 118.194.37.4 118.194.37.5 118.194.37.6 118.194.37.145 118.194.37.146 118.194.44.36 118.194.44.37 118.194.44.38 118.194.44.39 118.194.44.42 118.194.44.44 118.194.44.46 118.194.44.47 118.194.44.48 118.194.44.50 118.194.44.51 118.194.44.52 118.194.44.53 118.194.44.54 118.194.44.55 118.194.44.56 118.194.44.57 118.194.44.58 118.194.44.59 118.194.44.60 118.194.44.61 118.194.44.62 118.194.44.45 14.152.80.145 14.17.94.34 14.17.94.35 14.17.94.36 14.17.94.37 14.17.94.38 14.17.94.39 14.17.94.40 14.17.94.42 14.17.94.46 202.104.174.113 123.56.101.21 123.56.101.33 123.56.106.76 182.92.213.195 203.195.217.192 172.16.12.2 113.105.175.66 113.105.175.67 113.105.175.68 172.16.240.96)
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

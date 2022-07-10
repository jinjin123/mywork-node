#!/bin/bash
size=`/bin/df -h | grep "data" | awk '{print $4}'| awk -F '%' '{print $1}'`
mongodb3=`/usr/bin/du -sh /data/mongodb3/ | awk -F "G" '{print $1}'`
if [ $size -ge 90 ] || [ $mongodb3 -gt 320 ]
then
        /usr/bin/mongod --shutdown --dbpath /data/mongodb3
        /bin/rm -rf  /data/mongodb3/Ask.*  && /bin/rm -rf  /data/mongodb3/Askm.*
        /usr/bin/mongod --dbpath=/data/mongodb3 --port 4444 --logpath=/data/mongodb3/logs --fork
        if [ $? -eq 0 ]
        then
                exit
        else
                echo "error" >> /data/error.log

        fi
else
        exit
fi

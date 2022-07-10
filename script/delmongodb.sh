#!/bin/bash
use=`/bin/df | /bin/grep data | /bin/awk '{print $4}' | /bin/cut -d% -f1`

if [ $use -gt 93 ];then
        sql="db.dropDatabase();"
        /bin/echo "$sql"|/usr/bin/mongo 127.0.0.1:27017/search --shell
fi

#!/bin/bash

Diskused=`df -h | grep '\/data' | awk {'print $4'}|cut -d % -f 1`
res=0
judge=0

if [ $Diskused -gt 90 ]
then
  echo "files in /data/mongodb will be deleted! "
  res=1
  echo "please input judge's value,0 represent NO,1 represent YES"
  read judge
else
  echo "mongodb is normal,congratulations!"
  exit 0
fi


if [ $judge -eq 1 ] && [ $res -eq 1 ]
then
   echo "mongodb will be shutdown"
   sleep(3)
   service mongod stop
   rm -rf /data/mongodb/Ask.*
   mongod -f /etc/mongod.conf
fi

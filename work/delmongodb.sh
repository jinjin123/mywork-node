#!/bin/bash
use=`/bin/df | /bin/grep data | /bin/awk '{print $4}' | /bin/cut -d% -f1`

if [ $use -gt 93 ];then
        sql="db.dropDatabase();"
        /bin/echo "$sql"|/usr/bin/mongo 127.0.0.1:27017/search --shell
fi

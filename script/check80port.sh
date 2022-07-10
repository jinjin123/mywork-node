#!/bin/bash
url='http://127.0.0.1/'

HTTP_CODE=`/usr/bin/curl -o /dev/null -s -w "%{http_code}" "${url}"`
#echo $HTTP_CODE

if [ $HTTP_CODE != 200 ];then
        /bin/date +%Y%m%d-%H:%M:%S
        /bin/echo 'no'
fi

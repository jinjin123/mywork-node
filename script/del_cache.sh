#!/bin/bash
black="/var/jkcache/black/"
path="/var/jkcache/proxy_cache_dir_bak/proxy_cache_dir1"
cd $path
for i in `ls`
do
        cd ${i}
        while true
        do
                /bin/ls  | xargs -i /bin/rm -rf  {}
                /bin/du -sh $(pwd) | awk -F "." '{print $1}' && if [size - eq 4 ];then continue ;else /bin/ls |xargs -i /bin/rm -rf {}; fi
        done
                /bin/rm -rf ${path}\/${i}

done

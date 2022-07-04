#!/bin/bash
path="/data/jkcache/proxy_cache_dir3_bak/"
cd $path
for i in `ls`
do
        cd $i
        for b in `ls`
        do
                /bin/ls $b | xargs -i /bin/rm -rf {}
                sleep 10
                /bin/rm -rf $b
        done
                /bin/rm -rf ${path}\/${i}
done

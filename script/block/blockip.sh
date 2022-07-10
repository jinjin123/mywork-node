#!/bin/bash
fip=`/usr/bin/tail -50 /var/log/nginx/access.log | grep -v "127.0.0.1" | awk '{print $1,$9}' |  awk '$2 ~ /(500|404)/ {print $1,$2}'| uniq -c | awk '$1>10{print $2}'`
ext=`/usr/sbin/iptables -L INPUT | awk 'NR>3{print $4}'`
for i in  $fip
do
        [[ $ext =~ $i ]] && echo "exit" >/dev/null || /usr/sbin/iptables -A INPUT -s  $i  -p TCP -j DROP
done

#xargs -I{} /usr/sbin/iptables -A INPUT -s {} -p TCP -j DROP

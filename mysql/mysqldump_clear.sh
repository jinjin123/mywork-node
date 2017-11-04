#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/app/mysql/bin
#mysqlip=`docker exec -ti mysql bash -c  "ip a | grep eth0 | awk 'NR!=1{print $1}'|sed 's/scope\|global\|inet\|eth0//g'| sed 's#/[0-9]\{0,2\}##g' "`
#echo `docker exec -ti mysql bash -c  "ip a | grep eth0 | awk 'NR!=1{print $1}'|sed 's/scope\|global\|inet\|eth0//g'| sed 's#/[0-9]\{0,2\}##g'|  sed 's/^[][ ]*//g'|sed 's/[][ ]*//g'"` > /root/scripts/dbhost.txt


#docker exec  -ti mysql bash -c "cd /var/lib/mysql/ && mysqldump -uroot -pSpark123!   --max_allowed_packet=2048M  zkfecp | gzip > tvbackup`date +%Y%m%d`.sql.gz"
cd /data/backup/
#mysqldump -uroot -pSpark123!   -h 172.17.0.12 --max_allowed_packet=2048M  zkfecp | gzip > tvbackup`date +%Y%m%d`.sql.gz
mysqldump  -h dianzicanpai.mysqldb.chinacloudapi.cn -u dianzicanpai%spark -p'ine^hPsSWm8g!sh$Zn&4QA%D$L@DbwQ2'  --max_allowed_packet=2048M spark-emenu   | gzip > tvbackup`date +%Y%m%d`.sql.gz
#mv /mnt/resource/mysql/tvbackup`date +%Y%m%d`.sql.gz /data/backup/

#Delete the backups more than 7 days.
cd /data/backup
find . -mtime +14 -name '*.sql.gz' -exec rm {} \;

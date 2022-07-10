#!/bin/sh

## version 1.0

da=`date +%y%m%d%H%S`
#ip=`/sbin/ifconfig|grep 'addr:10'|awk -F ":" '{print $2}'|awk '{print $1}'`
h=sm12g5l9d32eyun.cjwa2zciaejp.rds.cn-north-1.amazonaws.com.cn
user="keithyau"
pd="thomas123"
#Mysql Backup Full
MysqlBackupFullPath="/home/ec2-user/hailong/gtdx_gp2_dbbackup"
#Backup Log Save Time
BackupSaveCycle=+2
#targetip='115.182.78.91'
#if [ ! -d /data/dbbackup ]
#then
#mkdir -p "/data/dbbackup"
#fi
cd $MysqlBackupFullPath
echo "=========================================================" >>$MysqlBackupFullPath/bak.log
echo "--------------Mysql Backup Full ------------ "  >>$MysqlBackupFullPath/bak.log
echo "start DB backup" >>$MysqlBackupFullPath/bak.log
echo $da>>$MysqlBackupFullPath/bak.log
echo `date +%Y%m%d%H%M%S`>>$MysqlBackupFullPath/bak.log
echo "." >>$MysqlBackupFullPath/bak.log
echo "." >>$MysqlBackupFullPath/bak.log
mysql -h$h -u$user -p$pd -e "show databases" |grep -v 'mysql\|test\|information_schema\|Database\|performance_schema'  > dblist
db=`cat dblist|awk  '{printf $0" "}'`
## master
paramm=" -u$user -p$pd -h$h --add-drop-table --add-locks --set-charset --create-options --disable-keys -e --quick --triggers -R --hex-blob --single-transaction --default-character-set=utf8 "
## slave
#params=" -u$user -p$pd -h$ip --opt -e --triggers --default-character-set=utf8 -R --hex-blob"

 #mysql -uroot -p$pd -e "show slave status\G;" > /data/dbbackup/slavestatus.log

#if [ -s /data/dbbackup/slavestatus.log ]
# then
#mysqldump $paramm --databases $db |gzip >$MysqlBackupFullPath/$h_$da.sql.gz
mysqldump $paramm --databases $db |gzip >$MysqlBackupFullPath/$h_$da.sql.gz
#else
#mysqldump $paramm --databases $db |gzip >$MysqlBackupFullPath/CC_$ip_$da.sql.gz
#fi

sleep 1
echo "." >>$MysqlBackupFullPath/bak.log
echo "." >>$MysqlBackupFullPath/bak.log
echo `date +%Y%m%d%H%M%S`>>$MysqlBackupFullPath/bak.log
echo "end DB backup" >>$MysqlBackupFullPath/bak.log
find $MysqlBackupFullPath -name \*.sql.gz -mtime $BackupSaveCycle -exec rm {} \;>>$MysqlBackupFullPath/bak.log




####aws to s3##

aws s3 sync /home/ec2-user/hailong/gtdx_gp2_dbbackup s3://sql/generalplatform/production/gtdx_gp2

#scp -P 58422 /data/dbbackup/CC_$ip_$da.sql.gz  root@$targetip:/app/rsyncsvr/gamedevQA/cc/db/CC_$ip_$da.sql.gz

#cd  /app/dbbackup/data/
#rm -rf *.sql.gz
#sleep 1
#复制当天数据库备份文件 到 上传数据备份中心路径下
#cp $MysqlBackupFullPath/LL_"$ip"_$da.sql.gz /app/dbbackup/data/


# gzip -d $MysqlBackupFullPath/CC_"$ip"_$da.sql.gz
#mysql -uroot -h$ip -p$pd  <  $MysqlBackupFullPath/CC_$ip_$da.sql

#sed -i '/backupdb/d' /var/spool/cron/root && echo "22 03 * * * sh /app/scripts/backupdb.sh " >> /var/spool/cron/root

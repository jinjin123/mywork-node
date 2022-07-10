#!/bin/bash
##脚本用于检查172.16.103.203的同步情况
##如果出现表不存在的问题，一般是主库更改了表名，需要手动拉取改变后的新表
##拉取新表后要跳过之前的错误，恢复同步状态,目前只检查189-203的同步
###by ltm
###date=20170323
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/app/mysql/bin
#set -x
##检查同步状态，是否有表不存在的错误,把错误写入文件
mysql -uroot -pSpark123! -e "SHOW SLAVE STATUS\G"|awk -F "['.]" '$1~/Last_SQL_Error/&&$(NF-1)~/exist/''{print$3,$4}' >noexist.list
if [ ! -s noexist.list ];then
echo "list is null"
exit
fi

Data188=`awk '$1~/de|payment|marketing/''{print$1}' noexist.list`
Table188=`awk '$1~/de|payment|marketing/''{print$2}' noexist.list`
if [ ! "$Data188" = "" ]; then
mysqldump -uroot -profiTKEhk6+d -h172.16.103.188 $Data188 $Table188 > $Table188.sql
#导入前停止对应channel的同步
mysql -uroot -pSpark123! -e "stop slave for channel 'master-1';"
mysql -uroot -pSpark123! $Data188 < $Table188.sql
#导入完成后开启slave同步
mysql -uroot -pSpark123! -e "SET GLOBAL SQL_SLAVE_SKIP_COUNTER = 1;"
mysql -uroot -pSpark123! -e "start slave for channel 'master-1';"
rm -rf  $Table188.sql
fi

Data207=`awk '$1~/oc|ocrp/''{print$1}' noexist.list`
Table207=`awk '$1~/co|ocrp/''{print$2}' noexist.list`
if [ ! "$Data207" = "" ]; then
#mysqldump -uroot -pnewpos -h172.16.103.207 $Data207 $Table207 > $Table207.sql
#导入前停止对应channel的同步
#mysql -uroot -pSpark123! -e "stop slave for channel 'master-2';"
#mysql -uroot -pSpark123! $Data207 < $Table207.sql
#导入完成后开启slave同步
#mysql -uroot -pSpark123! -e "SET GLOBAL SQL_SLAVE_SKIP_COUNTER = 1;"
#mysql -uroot -pSpark123! -e "start slave for channel 'master-2';"
#rm -rf  $Table207.sql
exit
fi

Data121=`awk '$1~/crm|erp/''{print$1}' noexist.list`
Table121=`awk '$1~/crm|erp/''{print$2}' noexist.list`
if [ ! "$Data121" = "" ]; then
mysqldump -uroot -ptp8p91OoW8m -h172.16.103.123 $Data121 $Table121 > $Table121.sql
#导入前停止对应channel的同步
mysql -uroot -pSpark123! -e "stop slave for channel 'master-3';"
mysql -uroot -pSpark123! $Data121 < $Table121.sql
#导入完成后开启slave同步
mysql -uroot -pSpark123! -e "SET GLOBAL SQL_SLAVE_SKIP_COUNTER = 1;"
mysql -uroot -pSpark123! -e "start slave for channel 'master-3';"
rm -rf  $Table121.sql
exit
fi

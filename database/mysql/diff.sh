#!/bin/bash                                                                                                                                                                                   
##脚本用于补单到203，检查2小时前                                                                                                                                                                           
###使用例子 ：bash budan.sh                                                                                                                                                                        
###date=20170527                                                                                                                                                                              
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/app/mysql/bin                                                                                                       
#set -x                                                                                                                                                                                       
startdate=`date +'%F'`                                                                                                                                                                        
enddate=`date -d '-1 hour' +'%F %T'`                                                                                                                                                          
dotime=`date +%F_%H:%M`                                                                                                                                                                       
cd /root/scripts/bak/                                                                                                                                                                         
#日志保存的目录                                                                                                                                                                                      
LOG_DIR=/var/log/budan                                                                                                                                                                        
LOG_FILE=$LOG_DIR/budan.log                                                                                                                                                                   
if [ ! -d $LOG_DIR ];then                                                                                                                                                                     
mkdir -p $LOG_DIR                                                                                                                                                                             
echo >$LOG_FILE                                                                                                                                                                               
fi                                                                                                                                                                                            
if [ ! -f "$LOG_FILE" ];then                                                                                                                                                                  
echo >$LOG_FILE                                                                                                                                                                               
fi                                                                                                                                                                                            
#检查203和207订单的状态，比对哪些不一致                                                                                                                                                                       
mysql -ureadonly -pAZTfjuCFoppEC6wR -h172.16.103.203 -e "use oc;select m.orderId, m.storeId, m.storeName, m.orderStatus, m.payStatus, m.orderSource, m.totalAmount, m.dicountAmount, m.freight
, m.payAmount, m.orderPlatformSource, m.addtime, m.payType from order_master m where m.orderStatus = 4 and m.payStatus = 1 and addtime between '$startdate 00:00:00' and '$enddate';">203.list
mysql -ureadonly -preadonly -h172.16.103.207 -e "use oc;select m.orderId, m.storeId, m.storeName, m.orderStatus, m.payStatus, m.orderSource, m.totalAmount, m.dicountAmount, m.freight, m.payA
mount, m.orderPlatformSource, m.addtime, m.payType from order_master m where m.orderStatus = 4 and m.payStatus = 1 and addtime between '$startdate 00:00:00' and '$enddate';">207.list        
diff 203.list 207.list|awk '{print$2}'>diff.list                                                                                                                                              
if [ ! -s diff.list ];then                                                                                                                                                                    
echo "list is null,不存在需要补单的订单"                                                                                                                                                                
exit                                                                                                                                                                                          
fi                                                                                                                                                                                            
sed -i '/^$/d' diff.list                                                                                                                                                                      
for i in `cat diff.list`                                                                                                                                                                      
do                                                                                                                                                                                            
cat 203.list |grep $i                                                                                                                                                                         
if [ "$?" -ne 0 ];then                                                                                                                                                                        
#mysqldump -uroot -pnewpos -h172.16.103.207 --single-transaction --skip-add-drop-table --no-create-info -w "orderId='$i'" oc order_master >$i.sql                                             
#mysql -uroot -pSpark123! -h172.16.103.203 oc <$i.sql                                                                                                                                         
#echo  "$i   补单成功 $dotime" >>$LOG_FILE                                                                                                                                                        
echo  "$i   订单漏单，不存在203列表 $dotime" >>$LOG_FILE                                                                                                                                                
#rm -rf $i.sql                                                                                                                                                                                
else                                                                                                                                                                                          
echo "$i   订单已经存在$dotime" >>$LOG_FILE                                                                                                                                                         
fi                                                                                                                                                                                            
done

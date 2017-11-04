#!/bin/bash                                                                                                                                                                                 
##检查memcache_fe连接数，如果达到阀值就重启memcache_fe服务                                                                                                                                                   
##添加到cron里每10分钟自动检查                                                                                                                                                                         
##*/10 * * * * /bin/bash /root/scripts/check-memcache.sh  >/dev/null 2>&1                                                                                                                   
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin                                                                                                                    
#set -x                                                                                                                                                                                     
#日志保存的目录                                                                                                                                                                                    
LOG_DIR=/var/log/check-memcache                                                                                                                                                             
LOG_FILE=$LOG_DIR/check-memcache.log                                                                                                                                                        
if [ ! -d $LOG_DIR ];then                                                                                                                                                                   
mkdir -p $LOG_DIR                                                                                                                                                                           
echo >$LOG_FILE                                                                                                                                                                             
fi                                                                                                                                                                                          
if [ ! -f "$LOG_FILE" ];then                                                                                                                                                                
echo >$LOG_FILE                                                                                                                                                                             
fi                                                                                                                                                                                          
sed -i '/^$/d' $LOG_FILE                                                                                                                                                                    
                                                                                                                                                                                            
CN=`netstat -na | grep 11214  | grep ESTABLISHED | wc -l`                                                                                                                                   
if [ "$CN" -le 10000 ];then                                                                                                                                                                 
echo "$(date +%F' '%T)  $CN低于阀值10000，跳出检查">>$LOG_FILE                                                                                                                                       
exit                                                                                                                                                                                        
else                                                                                                                                                                                        
echo "$(date +%F' '%T)   $CN高于阀值10000，重启memcache_fe服务">>$LOG_FILE                                                                                                                           
systemctl restart memcache_fe                                                                                                                                                               
fi                         

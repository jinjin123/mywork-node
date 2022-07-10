#!/bin/bash                                                                                                                                                                                   
##脚本用于检查172.16.103.203的同步情况                                                                                                                                                                   
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/app/mysql/bin                                                                                                       
set -x                                                                                                                                                                                        
##检查同步,如果同步停止，重新启动同步                                                                                                                                                                          
mysql -uroot -pSpark123! -e "SHOW SLAVE STATUS\G"|awk -F ":" '$1~/Running/&&$2~/No/''{print$0}' >noexist.list                                                                                 
if [ ! -s noexist.list ];then                                                                                                                                                                 
echo "list is null"                                                                                                                                                                           
exit                                                                                                                                                                                          
else                                                                                                                                                                                          
mysql -uroot -pSpark123! -e "start slave;"                                                                                                                                                    
echo "start slave"                                                                                                                                                                            
fi  

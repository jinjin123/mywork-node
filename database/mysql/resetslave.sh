#!/bin/bash                                                                                                                                                                                   
###用于重建slave同步                                                                                                                                                                                
###date=20170322                                                                                                                                                                              
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/app/mysql/bin                                                                                                       
set -x                                                                                                                                                                                        
USER='root'                                                                                                                                                                                   
IP189='172.16.103.189'                                                                                                                                                                        
IP121='172.16.103.123'                                                                                                                                                                        
IP207='172.16.103.207'                                                                                                                                                                        
Password189='rofiTKEhk6+d'                                                                                                                                                                    
Password203='Spark123!'                                                                                                                                                                       
Password121='tp8p91OoW8m'                                                                                                                                                                     
Password207='newpos'                                                                                                                                                                          
#查看189master状态，记录master_log_file='mysql2-bin.000001',master_log_pos=757                                                                                                                       
Master_log_file=`mysql -u$USER -p$Password189 -h$IP189 -e " show master status\G"|awk '$1~/File:/''{printf$2}'`                                                                               
Master_log_pos=`mysql -u$USER -p$Password189 -h$IP189 -e " show master status\G"|awk '$1~/Position:/''{printf$2}'`                                                                            
#先停止203的slave master-1同步                                                                                                                                                                      
#mysql -u$USER -p$Password203  -e "stop slave  for channel 'master-1';"                                                                                                                       
#修改slave同步状态                                                                                                                                                                                  
#mysql -u$USER -p$Password203 -e "change master to master_host='$IP189',master_user='$USER',master_password='$Password189', master_log_file='$Master_log_file',master_log_pos=$Master_log_pos 
for channel 'master-1';"                                                                                                                                                                      
#修改完成后开启203的slave master-1同步                                                                                                                                                                  
#mysql -u$USER -p$Password203  -e "start slave  for channel 'master-1';"                                                                                                                      
                                                                                                                                                                                              
#查看207master状态，记录master_log_file='mysql2-bin.000001',master_log_pos=757                                                                                                                       
Master_log_file=`mysql -u$USER -p$Password207 -h$IP207 -e " show master status\G"|awk '$1~/File:/''{printf$2}'`                                                                               
Master_log_pos=`mysql -u$USER -p$Password207 -h$IP207 -e " show master status\G"|awk '$1~/Position:/''{printf$2}'`                                                                            
#先停止203的slave master-2同步                                                                                                                                                                      
#mysql -u$USER -p$Password203  -e "stop slave  for channel 'master-2';"                                                                                                                       
#修改slave同步状态                                                                                                                                                                                  
#mysql -u$USER -p$Password203 -e "change master to master_host='$IP207',master_user='$USER',master_password='$Password207', master_log_file='$Master_log_file',master_log_pos=$Master_log_pos 
for channel 'master-2';"                                                                                                                                                                      
#修改完成后开启203的slave master-1同步                                                                                                                                                                  
#mysql -u$USER -p$Password203  -e "start slave  for channel 'master-2';"                                                                                                                      
                                                                                                                                                                                              
#查看121master状态，记录master_log_file='mysql2-bin.000001',master_log_pos=757                                                                                                                       
Master_log_file=`mysql -u$USER -p$Password121 -h$IP121 -e " show master status\G"|awk '$1~/File:/''{printf$2}'`                                                                               
Master_log_pos=`mysql -u$USER -p$Password121 -h$IP121 -e " show master status\G"|awk '$1~/Position:/''{printf$2}'`                                                                            
#先停止203的slave master-3同步                                                                                                                                                                      
mysql -uroot -pSpark123! -e "stop slave  for channel 'master-3';"                                                                                                                             
#修改slave同步状态                                                                                                                                                                                  
mysql -u$USER -p$Password203 -e "change master to master_host='172.16.103.123',master_user='root',master_password='tp8p91OoW8m', master_log_file='$Master_log_file',master_log_pos=$Master_log
_pos for channel 'master-3';"                                                                                                                                                                 
#修改完成后开启203的slave master-3同步                                                                                                                                                                  
mysql -u$USER -p$Password203  -e "start slave  for channel 'master-3';"  

#!/bin/bash                                                                                                                                                                                   
###删除以DROP TABLE IF EXISTS开头的行                                                                                                                                                                
###update 修改使用参数循环dump123的数据导入203                                                                                                                                                             
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/app/mysql/bin                                                                                                       
set -x                                                                                                                                                                                        
USER='root'                                                                                                                                                                                   
Password123='tp8p91OoW8m'                                                                                                                                                                     
Password203='Spark123!'                                                                                                                                                                       
TABLES='field_data_field_deposit_card_no                                                                                                                                                      
field_data_field_deposit_type                                                                                                                                                                 
field_data_field_pay_status                                                                                                                                                                   
field_data_field_deposit_store_id                                                                                                                                                             
field_data_field_deposit_status                                                                                                                                                               
field_data_field_deposit_amount                                                                                                                                                               
field_data_field_deposit_channel                                                                                                                                                              
field_data_field_deposit_cancel_no                                                                                                                                                            
field_data_field_deposit_no                                                                                                                                                                   
field_data_field_deposit_cancel_store_id'                                                                                                                                                     
#导入前停止slave同步                                                                                                                                                                                 
#mysql -uroot -pSpark123! -e "stop slave for channel 'master-3';"                                                                                                                             
for i in $TABLES                                                                                                                                                                              
do                                                                                                                                                                                            
mysqldump -u$USER -p$Password123 --max_allowed_packet=2048M -h172.16.103.121 crm $i > $i.sql                                                                                                  
#删除以DROP TABLE IF EXISTS开头的行，删除会导致导入的时候表存在无法导入                                                                                                                                                
#sed -i '/^DROP TABLE IF EXISTS/d' $i.sql                                                                                                                                                     
mysql -u$USER -p$Password203 crm < $i.sql                                                                                                                                                     
rm -rf $i.sql                                                                                                                                                                                 
done                                                                                                                                                                                          
#导入完成后开启slave同步                                                                                                                                                                               
#mysql -uroot -pSpark123! -e "start slave for channel 'master-3';"                                                                                                                            
exit    

#!/bin/bash                                                                                                                                                                                   
###把oc库的tables导出保存为csv格式，上传到百度云盘，给ken lin使用                                                                                                                                                   
###date=20170313                                                                                                                                                                              
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/app/mysql/bin                                                                                                       
set -x                                                                                                                                                                                        
tables='order_master order_detail order_discount order_meal_detail'                                                                                                                           
mysql_uer=root                                                                                                                                                                                
mysql_passwd=Spark123!                                                                                                                                                                        
for i in $tables                                                                                                                                                                              
do                                                                                                                                                                                            
mysql -u$mysql_uer -p$mysql_passwd <<EOF                                                                                                                                                      
use oc                                                                                                                                                                                        
select * from $i                                                                                                                                                                              
into outfile '/tmp/$i.csv'                                                                                                                                                                    
fields terminated by ',' optionally enclosed by '"' escaped by '"'                                                                                                                            
lines terminated by '\r\n';                                                                                                                                                                   
EOF                                                                                                                                                                                           
done                                                                                                                                                                                          
exit 

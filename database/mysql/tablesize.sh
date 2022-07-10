#!/bin/bash                                                                                                                                                                                 
##自动统计189、121、125、207、209、133、203数据表大小                                                                                                                                                      
##添加到cron里每天24自动检查                                                                                                                                                                          
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin                                                                                                                    
##set -x                                                                                                                                                                                    
cd /home/spadmin/statistics/                                                                                                                                                                
##统计203                                                                                                                                                                                     
#oc                                                                                                                                                                                         
mysql -uroot -pSpark123! -h172.16.103.203 -e "use information_schema;select table_name, concat(round((data_length/1024/1024),2),'MB') as data_mb , concat(round((index_length/1024/1024),2),
'MB')  as index_mb, concat(round(((data_length+index_length)/1024/1024),2),'MB') as all_mb from tables where table_schema = 'oc' order by data_length desc limit 10;">203oc$(date -d "1 day 
ago" +"%m%d").txt                                                                                                                                                                           
#erp                                                                                                                                                                                        
mysql -uroot -pSpark123! -h172.16.103.203 -e "use information_schema;select table_name, concat(round((data_length/1024/1024),2),'MB') as data_mb , concat(round((index_length/1024/1024),2),
'MB')  as index_mb, concat(round(((data_length+index_length)/1024/1024),2),'MB') as all_mb from tables where table_schema = 'erp' order by data_length desc limit 10;">203erp$(date -d "1 da
y ago" +"%m%d").txt                                                                                                                                                                         
#crm                                                                                                                                                                                        
mysql -uroot -pSpark123! -h172.16.103.203 -e "use information_schema;select table_name, concat(round((data_length/1024/1024),2),'MB') as data_mb , concat(round((index_length/1024/1024),2),
'MB')  as index_mb, concat(round(((data_length+index_length)/1024/1024),2),'MB') as all_mb from tables where table_schema = 'crm' order by data_length desc limit 10;">203crm$(date -d "1 da
y ago" +"%m%d").txt                                                                                                                                                                         
##统计133                                                                                                                                                                                     
#datacache                                                                                                                                                                                  
mysql -uroot -pSpark123! -h172.16.103.133 -e "use information_schema;select table_name, concat(round((data_length/1024/1024),2),'MB') as data_mb , concat(round((index_length/1024/1024),2),
'MB')  as index_mb, concat(round(((data_length+index_length)/1024/1024),2),'MB') as all_mb from tables where table_schema = 'datacache' order by data_length desc limit 10;">133datacache$(d
ate -d "1 day ago" +"%m%d").txt                                                                                                                                                             
#solidified                                                                                                                                                                                 
mysql -uroot -pSpark123! -h172.16.103.133 -e "use information_schema;select table_name, concat(round((data_length/1024/1024),2),'MB') as data_mb , concat(round((index_length/1024/1024),2),
'MB')  as index_mb, concat(round(((data_length+index_length)/1024/1024),2),'MB') as all_mb from tables where table_schema = 'solidified' order by data_length desc limit 10;">133solidified$
(date -d "1 day ago" +"%m%d").txt                                                                                                                                                           
##统计121crm                                                                                                                                                                                  
mysql -uroot -ptp8p91OoW8m -h172.16.103.121 -e "use information_schema;select table_name, concat(round((data_length/1024/1024),2),'MB') as data_mb , concat(round((index_length/1024/1024),2
),'MB')  as index_mb, concat(round(((data_length+index_length)/1024/1024),2),'MB') as all_mb from tables where table_schema = 'crm' order by data_length desc limit 10;">121crm$(date -d "1 
day ago" +"%m%d").txt                                                                                                                                                                       
##统计125erp                                                                                                                                                                                  
mysql -uroot -ptp8p91OoW8m -h172.16.103.125 -e "use information_schema;select table_name, concat(round((data_length/1024/1024),2),'MB') as data_mb , concat(round((index_length/1024/1024),2
),'MB')  as index_mb, concat(round(((data_length+index_length)/1024/1024),2),'MB') as all_mb from tables where table_schema = 'erp' order by data_length desc limit 10;">125erp$(date -d "1 
day ago" +"%m%d").txt                                                                                                                                                                       
##统计207oc                                                                                                                                                                                   
mysql -uroot -pnewpos -h172.16.103.207 -e "use information_schema;select table_name, concat(round((data_length/1024/1024),2),'MB') as data_mb , concat(round((index_length/1024/1024),2),'MB
')  as index_mb, concat(round(((data_length+index_length)/1024/1024),2),'MB') as all_mb from tables where table_schema = 'oc' order by data_length desc limit 10;">207oc$(date -d "1 day ago
" +"%m%d").txt                                                                                                                                                                              
#Delete the backups more than 7 days.                                                                                                                                                       
#find /home/spadmin/statistics/ -mtime +21 -name '*.txt' -exec rm {} \;  

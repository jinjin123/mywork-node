#!/bin/bash                                                                                                                                                                                   
##脚本用于检查172.16.103.203的同步情况                                                                                                                                                                   
###date=20170526                                                                                                                                                                              
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/app/mysql/bin                                                                                                       
#set -x                                                                                                                                                                                       
##检查同步,展示同步情况                                                                                                                                                                                 
mysql -uroot -pSpark123! -e "SHOW SLAVE STATUS\G"| grep -E "Running|Master_Log_File|Behind|Log_Pos|Last_SQL_Error:|Behind" >status.list                                                       
if [ ! -s status.list ];then                                                                                                                                                                  
echo "list is null"                                                                                                                                                                           
exit                                                                                                                                                                                          
fi                                                                                                                                                                                            
echo "____________________________________________________________"                                                                                                                           
#检查de同步状态                                                                                                                                                                                     
sed -n '1,11p' status.list|awk -F ":" '$1~/Running/&&$2~/No/''{print$0}' >error.list                                                                                                          
if [ ! -s error.list ];then                                                                                                                                                                   
echo "189de同步到203状态为正常同步，Success，同步延迟为："                                                                                                                                                      
sed -n '1,11p' status.list|awk -F "['.]" '$1~/Seconds_Behind_Master/''{print$1,$2"s"}'                                                                                                        
else                                                                                                                                                                                          
echo "189de同步203状态为异常停止，faild!!!，错误为："                                                                                                                                                        
cat error.list                                                                                                                                                                                
sed -n '1,11p' status.list|awk -F "[:]" '$1~/Last_SQL_Error/''{print$0}'                                                                                                                      
fi                                                                                                                                                                                            
echo "____________________________________________________________"                                                                                                                           
#检查oc同步状态                                                                                                                                                                                     
sed -n '12,22p' status.list|awk -F ":" '$1~/Running/&&$2~/No/''{print$0}' >error.list                                                                                                         
if [ ! -s error.list ];then                                                                                                                                                                   
echo "207oc同步到203状态为正常同步，Success，同步延迟为："                                                                                                                                                      
sed -n '12,22p' status.list|awk -F "['.]" '$1~/Seconds_Behind_Master/''{print$1,$2"s"}'                                                                                                       
else                                                                                                                                                                                          
echo "207oc同步到203状态为异常停止，faild!!!，错误为："                                                                                                                                                       
cat error.list                                                                                                                                                                                
sed -n '12,22p' status.list|awk -F "['.]" '$1~/Last_SQL_Error/''{print$0}'                                                                                                                    
fi                                                                                                                                                                                            
echo "____________________________________________________________"                                                                                                                           
#检查crm同步状态                                                                                                                                                                                    
sed -n '23,33p' status.list|awk -F ":" '$1~/Running/&&$2~/No/''{print$0}' >error.list                                                                                                         
if [ ! -s error.list ];then                                                                                                                                                                   
echo "121crm同步到203状态为正常同步，Success，同步延迟为："                                                                                                                                                     
sed -n '23,33p' status.list|awk -F "['.]" '$1~/Seconds_Behind_Master/''{print$1,$2"s"}'                                                                                                       
else                                                                                                                                                                                          
echo "121crm同步到203状态为异常停止，faild!!!，错误为："                                                                                                                                                      
cat error.list                                                                                                                                                                                
sed -n '23,33p' status.list|awk -F "['.]" '$1~/Last_SQL_Error/''{print$0}'                                                                                                                    
fi                                                                                                                                                                                            
echo "____________________________________________________________"                                                                                                                           
#检查erp同步状态                                                                                                                                                                                    
sed -n '34,44p' status.list|awk -F ":" '$1~/Running/&&$2~/No/''{print$0}' >error.list                                                                                                         
if [ ! -s error.list ];then                                                                                                                                                                   
echo "125erp同步到203状态为正常同步，Success，同步延迟为："                                                                                                                                                     
sed -n '34,44p' status.list|awk -F "['.]" '$1~/Seconds_Behind_Master/''{print$1,$2"s"}'                                                                                                       
else                                                                                                                                                                                          
echo "125erp同步到203状态为异常停止，faild!!!，错误为："                                                                                                                                                      
cat error.list                                                                                                                                                                                
sed -n '34,44p' status.list|awk -F "['.]" '$1~/Last_SQL_Error/''{print$0}'                                                                                                                    
fi                                                                                                                                                                                            
echo "____________________________________________________________"                                                                                                                           
#检查marketing同步状态                                                                                                                                                                              
sed -n '45,55p' status.list|awk -F ":" '$1~/Running/&&$2~/No/''{print$0}' >error.list                                                                                                         
if [ ! -s error.list ];then                                                                                                                                                                   
echo "209marketing同步到203状态为正常同步，Success，同步延迟为："                                                                                                                                               
sed -n '45,55p' status.list|awk -F "['.]" '$1~/Seconds_Behind_Master/''{print$1,$2"s"}'                                                                                                       
else                                                                                                                                                                                          
echo "209marketing同步到203状态为异常停止，faild!!!，错误为："                                                                                                                                                
cat error.list                                                                                                                                                                                
sed -n '45,55p' status.list|awk -F "['.]" '$1~/Last_SQL_Error/''{print$0}'                                                                                                                    
fi                                                                                                                                                                                            
echo "____________________________________________________________"                                                                                                                           
#检查datacache同步状态                                                                                                                                                                              
sed -n '56,66p' status.list|awk -F ":" '$1~/Running/&&$2~/No/''{print$0}' >error.list                                                                                                         
if [ ! -s error.list ];then                                                                                                                                                                   
echo "133datacache同步到203状态为正常同步，Success，同步延迟为："                                                                                                                                               
sed -n '56,66p' status.list|awk -F "['.]" '$1~/Seconds_Behind_Master/''{print$1,$2"s"}'                                                                                                       
else                                                                                                                                                                                          
echo "133datacache同步到203状态为异常停止，faild!!!，错误为："                                                                                                                                                
cat error.list                                                                                                                                                                                
sed -n '56,66p' status.list|awk -F "['.]" '$1~/Last_SQL_Error/''{print$0}'                                                                                                                    
fi                                                                                                                                                                                            
echo "____________________________________________________________" 

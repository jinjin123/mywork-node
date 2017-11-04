#!/bin/bash                                                                                                                                                                                 
###  bind local port to dymanic  on remote pc create port  
while true                                                                                                                                                                                  
do                                                                                                                                                                                          
ssh -i /root/keys/sparkpad_test -D 0.0.0.0:9777 -Nv root@paymproxy.chinacloudapp.cn -p9523                                                                                                  
done 

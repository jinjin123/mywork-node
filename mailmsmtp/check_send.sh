#!/bin/bash                                                                                                                                                                                 
cd /etc/ansible/;echo "" >  /etc/ansible/1.out;sed -i '1d' /etc/ansible/1.out;cat /etc/ansible/resource  | grep -v 'backup' |  grep  'G' | awk '{print $5}' | awk  '{print $1}'  | awk -F '%
' '{if($1>70)  print '$1' >  "/etc/ansible/1.out" }'                                                                                                                                        
cd /etc/ansible/;if [ $(cat /etc/ansible/1.out | wc -l) -gt 0 ];then mutt -s "Dayily report if disk use > 70%  memory ->G" jimmy_jinjin@126.com  -c keithyau@sparkpad.com -c tmli@sparkpad.c
om -c jcyu@sparkpad.com -c wjyao@sparkpad.com -c jackychan@sparkpad.com  < /etc/ansible/resource ;else exit;fi                                                                              
#cd /etc/ansible/;echo "" >  /etc/ansible/1;sed -i '1d' /etc/ansible/1;cat /etc/ansible/0  | grep G | awk '{print $5}' | awk  '{print $1}'  | awk -F '%' '{if($1>10)  print '$1' >  "/etc/an
sible/1" }'                                                                                                                                                                                 
#cd /etc/ansible/;if [ $(cat /etc/ansible/1.out  | wc -l) > 0 ];then echo "monitor report  if disk use > 70%  memory ->G" |mutt -s "Dayily report" 1293813551@qq.com -c keithyau@sparkpad.co
m -c tmli@sparkpad.com -c jcyu@sparkpad.com -c wjyao@sparkpad.com -c jackychan@sparkpad.com -a /etc/ansible/disk.txt -a /etc/ansible/memory.txt;else exit;fi                                
#cd /etc/ansible/;if [ $(cat /etc/ansible/1.out  | wc -l) > 0 ];then echo "monitor report  if disk use > 70%  memory ->G" |mutt -s "Dayily report" 1293813551@qq.com -a /etc/ansible/disk.tx
t -a /etc/ansible/memory.txt;else exit;fi 

#!/bin/bash                                                                                                                                                                                 
ansible dmem -m shell -a "df -h |  awk -F '%' '{print \$1,\$2}' | awk 'BEGIN{a=70}{if(\$5>a)print \$1,\$2,\$3,\$4,\$5\"%\",\$6}';free -g" > /etc/ansible/resource                           
#ansible dmem -m shell -a "df -h |  awk -F '%' '{print \$1,\$2}' | awk 'BEGIN{a=70}{if(\$5>a)print \$1,\$2,\$3,\$4,\$5\"%\",\$6}'" > /etc/ansible/disk.txt                                  
#ansible dmem -m shell -a "free -g" > /etc/ansible/memory.txt                                                                                                                               
#echo "monitor report" |mutt -s "monitor" jimmy_jinjin@126.com  -a $1 -a $2                                                                                                                 
#echo "monitor report disk use > 60%  memory ->G" |mutt -s "Dayily report" 1293813551@qq.com -a /etc/ansible/disk.txt -a /etc/ansible/memory.txt                                            
#echo "monitor report  if disk use > 70%  memory ->G" |mutt -s "Dayily report" 1293813551@qq.com -c keithyau@sparkpad.com -c tmli@sparkpad.com -c jcyu@sparkpad.com -c wjyao@sparkpad.com -c
 jackychan@sparkpad.com -a /etc/ansible/disk.txt -a /etc/ansible/memory.txt

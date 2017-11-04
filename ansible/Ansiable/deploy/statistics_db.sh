echo "statistics for 133"
ansible 172.16.103.133 -m shell -a "du -sh /app/mysql/*|grep -E 'datacache|solidified'"|sed -n '2,3p'
echo "statistics for 203"
ansible 172.16.103.203 -m shell -a "du -sh /data/mysql/*/|grep -E 'erp|crm|oc'|grep -E -v 'erp040101|oc201702|ocrp'"|sed -n '2,6p'
echo "statistics for 121"
ansible 172.16.103.121 -m shell -a "du -sh /app/mysql/data/crm/"|sed -n '2,3p'
echo "statistics for 125"
ansible 172.16.103.125 -m shell -a "du -sh /app/mysql/data/erp/"|sed -n '2,3p'
echo "statistics for 207"
ansible 172.16.103.207 -m shell -a "du -sh /app/mysql/data/oc/"|sed -n '2,3p'

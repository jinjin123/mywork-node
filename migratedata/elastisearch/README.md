npm install elasticdump

elastisearch 7.8.0

#get all index
curl 'localhost:9200/_cat/indices?v'  | awk '{print $3}' > t


#output export command
#!/bin/bash
for x in `cat t`
do
	#echo  "elasticdump --input=http://localhost:9200/$x --output=$x.json --type=mapping --bulk=true" 
	echo  "elasticdump --input=http://localhost:9200/$x --output=$x.json --type=data --bulk=true" 
done

elasticdump --input=http://localhost:9200/dgcn-applicationaccess-pro-2021 --output=apppro.json --type=mapping --bulk=true


elasticdump  --input=/home/jin/下载/apppro.json  --output=http://localhost:9200/dgcn-applicationaccess-pro-2021 --type=mapping

#link
https://www.jianshu.com/p/bcd17c7affab
https://www.cnblogs.com/pilihaotian/p/5830754.html



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


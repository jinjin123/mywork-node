#!/bin/bash
db='cs
datascience
faculty
foundation
neuro
nyus_src_global
research
researchsymposium
shanghai
shwp
ssaml
staff
students
test
textbooks'
bkdir='/srv/www/dbbackup/'
dir=`date "+%Y-%m-%d"`
for x in $db
do
	/bin/mkdir -p ${bkdir}${dir}
	if [ $x = 'shanghai' ]
	then
		/usr/bin/mysqldump -uroot -proot $x --max_allowed_packet=2048M |gzip > ${bkdir}${dir}/stage_${x}_`date "+%Y-%m-%d"`.sql.gz
	else
	        /usr/bin/mysqldump -uroot -proot $x --max_allowed_packet=2048M |gzip > ${bkdir}${dir}/${x}_`date "+%Y-%m-%d"`.sql.gz
	fi
done
/usr/bin/aws s3 sync ${bkdir}${dir} s3://nyuproduction-shanghai/dbbackup/${dir}

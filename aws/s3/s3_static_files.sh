#!/bin/bash
tbooks='/srv/www/textbooks/public_html/sites/default/files/'
students='/srv/www/portals/public_html/sites/students.shanghai.nyu.edu/files/'
stage='/srv/www/stage/public_html/sites/default/files/'
staff='/srv/www/portals/public_html/sites/staff.shanghai.nyu.edu/files/'
researchsymposium='/srv/www/researchsymposium/public_html/sites/default/files/'
research='/srv/www/research/public_html/sites/default/files/'
neuro='/srv/www/neuro/public_html/sites/default/files/'
foundation='/srv/www/foundation/public_html/sites/default/files/'
faculty='/srv/www/portals/public_html/sites/faculty.shanghai.nyu.edu/file/'
datascience='/srv/www/major/public_html/sites/datascience.shanghai.nyu.edu/files/'
cs='/srv/www/major/public_html/sites/cs.shanghai.nyu.edu/files/'
tb='textbooks.shanghai.nyu.edu'
stu='students.shanghai.nyu.edu'
st='stage.shanghai.nyu.edu'
sta='staff.shanghai.nyu.edu'
rsy='researchsymposium.shanghai.nyu.edu'
re='research.shanghai.nyu.edu'
ne='neuro.shangahi.nyu.edu'
fo='foundation.shanghai.nyu.edu'
fa='faculty.shanghai.nyu.edu'
da='datascience.shanghai.nyu.edu'
css='cs.shanghai.nyu.edu'
for s in $tb $stu $st $st $rsy $re $ne $fo $fa $da $css
do
	if [ $s == 'textbooks.shanghai.nyu.edu' ]
	then
		/usr/bin/aws s3 sync $tbooks  s3://nyuproduction-shanghai/$s/files/
	elif [ $s == 'students.shanghai.nyu.edu' ]
	then
		/usr/bin/aws s3 sync $students  s3://nyuproduction-shanghai/$s/files/
	elif [ $s == 'stage.shanghai.nyu.edu' ]
	then
		/usr/bin/aws s3 sync $stage s3://nyuproduction-shanghai/$s/files/
	elif [ $s == 'staff.shanghai.nyu.edu' ]
	then
		/usr/bin/aws s3 sync $staff s3://nyuproduction-shanghai/$s/files/
	elif [ $s == 'researchsymposium.shanghai.nyu.edu' ]
	then
		/usr/bin/aws s3 sync $researchsymposium s3://nyuproduction-shanghai/$s/files/
	elif [ $s == 'research.shanghai.nyu.edu' ]
	then
		/usr/bin/aws s3 sync $research s3://nyuproduction-shanghai/$s/files/
	elif [ $s == 'neuro.shanghai.nyu.edu' ]
	then
		/usr/bin/aws s3 sync $neuro s3://nyuproduction-shanghai/$s/files/
	elif [ $s == 'foundation.shanghai.nyu.edu' ]
	then
		/usr/bin/aws s3 sync $foundation s3://nyuproduction-shanghai/$s/files/
	elif [ $s == 'faculty.shanghai.nyu.edu' ]
	then
		/usr/bin/aws s3 sync $faculty s3://nyuproduction-shanghai/$s/file/
	elif [ $s == 'datascience.shanghai.nyu.edu' ]
	then
		/usr/bin/aws s3 sync $datascience s3://nyuproduction-shanghai/$s/files/
	elif [ $s == 'cs.shanghai.nyu.edu' ]
	then
		/usr/bin/aws s3 sync $cs s3://nyuproduction-shanghai/$s/files/
	fi
done

#!/bin/bash
a="/600/600.bat"
for i in `seq 1 10`
do
	sed  -e "s/agent3/agent$i/g" $a | tee /600.bat
	cp -r /600  /test/600
	rm -rf /test/600/600.bat
	mv /600.bat /test/600/600.bat
	cd /test && zip -r $i.zip 600
	rm -rf /test/600
done

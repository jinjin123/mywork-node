#!/bin/bash

#Enable section
CC=1
#CRM=1
#MKT=1
#DE=1
#PMT=1
#FE=1
#ERP=1

if [ ! -z ${CC} ] && [ ${CC} -eq 1 ];
then
    echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    echo "Running for CC"
    cd /Users/chankongching/src/sparkpad/code/sparkpad-drupal-backend-cc
    git branch -l
    git pull mshen master
    git push origin sparkpad
fi
if [ ! -z ${CRM} ] && [ ${CRM} -eq 1 ];
then
	echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	echo "Running for CRM"
	cd /Users/chankongching/src/sparkpad/code/sparkpad-drupal-backend-crm
	git branch -l
	git pull mshen zkf3.0
	git push origin sparkpad
fi
if [ ! -z ${MKT} ] && [ ${MKT} -eq 1 ];
then
	echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	echo "Running for MKT"
	cd /Users/chankongching/src/sparkpad/code/sparkpad-drupal-backend-mkt
	git branch -l
	git pull mshen zkf-marketing-dev
	git push origin sparkpad
fi
if [ ! -z ${DE} ] && [ ${DE} -eq 1 ];
then
	echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	echo "Running for DE"
	cd /Users/chankongching/src/sparkpad/code/sparkpad-drupal-backend-de
	git branch -l
	git pull mshen dev
	git push origin sparkpad
fi
if [ ! -z ${PMT} ] && [ ${PMT} -eq 1 ];
then
	echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	echo "Running for PMT"
	cd /Users/chankongching/src/sparkpad/code/sparkpad-drupal-backend-pmt
	git branch -l
	git pull mshen zkf3.0
	git push origin sparkpad
fi
if [ ! -z ${FE} ] && [ ${FE} -eq 1 ];
then
	echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	echo "Running for FE"
	cd /Users/chankongching/src/sparkpad/code/sparkpad-symfony-frontend
	git branch -l
	git pull mshen dev
	git push origin sparkpad
fi

if [ ! -z ${ERP} ] && [ ${ERP} -eq 1 ];
then
        echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        echo "Running for FE"
        cd /Users/chankongching/src/sparkpad/code/sparkpad-drupal-backend-erp
        git branch -l
        git pull mshen master 
        git push origin sparkpad
fi

#!/bin/bash
file_name=$1
[[ $(egrep -wo "password=[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}'; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 1
[[ $(egrep -wo "SPRING_DATASOURCE_PASSWORD:[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 2
[[ $(egrep -wo "password value=[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}'; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 3
[[ $(egrep -wo "datasource.default.pwd=[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 4
[[ $(egrep -wo "pwd=[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 5
[[ $(egrep -wo "\,password =[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} |grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 6
[[ $(egrep -wo "\,password=[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 7
[[ $(egrep -wo "\,Password =[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 8
[[ $(egrep -wo "\,Password=[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 9
[[ $(egrep -wo "\, password =[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 10
[[ $(egrep -wo "\, password=[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 11
[[ $(egrep -wo "\, Password =[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 12
[[ $(egrep -wo "\, Password=[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 13
[[ $(egrep -wo "\;Password=[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 14
[[ $(egrep -wo "\; Password=[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 15
[[ $(egrep -wo "password:[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 16
[[ $(egrep -wo "password [\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} |grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 17
[[ $(egrep -wo "pwd:[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 19
[[ $(egrep -wo "pwd [\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 19
[[ $(egrep -wo "passwd:[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 20
[[ $(egrep -wo "passwd=[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} |  grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}'  ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 21
[[ $(egrep -wo "passwd [\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} |   grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 22
[[ $(egrep -wo "PASSWORD:[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 23
[[ $(egrep -wo "PASSWORD=[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 24
[[ $(egrep -wo "PASSWORD [\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 25
[[ $(egrep -wo "PWD:[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 26
[[ $(egrep -wo "PWD=[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 27
[[ $(egrep -wo "PWD [\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 28
[[ $(egrep -wo "password.AppSecretKey=[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 29
[[ $(egrep -wo "password.aid=[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 30
[[ $(egrep -wo "<password>=[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 31
[[ $(egrep -wo "oprpwdMaps=[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 32
[[ $(egrep -wo "elasticsearch.cluster.addresses.user=[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}'; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 33
[[ $(egrep -wo "amqp:[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]" ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 34
[[ $(egrep -wo '<property name="password" value="[\[0-9\]+]\*\*\*\*\*\*\*\*\*.[\[0-9\]+]"' ${file_name} | grep -o "*" | grep -c "*" | awk '{if($0>10 ||$0< 10 ) exit 1;}' ; echo $? ) == 0 ]] && echo 0>/dev/null || exit 1
echo 35

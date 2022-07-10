#!/bin/bash

CpuTotal=`grep processor /proc/cpuinfo | wc -l`;
MemKiB=`grep MemTotal /proc/meminfo | tr -s " " | cut -d" " -f2`;
MemMiB=${MemKiB}/1024;
DiskKiB=`df /data | grep data | tr -s " " | cut -d" " -f4`;
DiskGiB=${DiskKiB}/1024/1024;
Gate=`ip route list | grep via | tr -s " " | cut -d" " -f3 | uniq | egrep "^10|172|192"`;
SubNet=`ip route list | grep kernel  | tr -s " " | cut -d" " -f1 | uniq | egrep "^10|172|192" | cut -d"/" -f1`;
Mask=`ip route list | grep kernel  | tr -s " " | cut -d" " -f1 | uniq | egrep "^10|172|192" | cut -d"/" -f2`;

echo $CpuTotal
echo $MemKib
echo $DiskKiB
echo $DiskGiB
echo $Gate
echo $SubNet
echo $Mask


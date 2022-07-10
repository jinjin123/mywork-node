#!/bin/bash

cur_path=$(dirname $(which $0))

cpu_num=`cat /proc/stat | grep cpu | sed 1d | wc -l`
cpu_hz=`cat /proc/cpuinfo | grep 'cpu MHz' | tail -n1 | awk -F':' '{print $2}'`

echo "cpu 核心数量: "$cpu_num
echo "cpu 频率: "$cpu_hz


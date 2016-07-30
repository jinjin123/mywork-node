#!/bin/bash
logs_path="/usr/local/tengine/logs/"
#以前的日志文件
log_name="www.jianke.com.log"
log_name1="baojian.jianke.com.log"
log_name2="ilife.jianke.com.log"
pid_path="/usr/local/tengine/logs/nginx.pid"
/bin/mv ${logs_path}${log_name} ${logs_path}${log_name}_$(date --date="LAST   DAY" +"%Y-%m-%d").log
/bin/mv ${logs_path}${log_name1} ${logs_path}${log_name1}_$(date --date="LAST   DAY" +"%Y-%m-%d").log
/bin/mv ${logs_path}${log_name2} ${logs_path}${log_name2}_$(date --date="LAST   DAY" +"%Y-%m-%d").log
kill -USR1 `cat ${pid_path}`
cd /usr/local/tengine/logs/
rm -rf *.log_*.log

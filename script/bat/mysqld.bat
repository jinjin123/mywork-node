@ECHO OFF
mysqladmin -u root password "root"
ping 127.0.0.1 -n 1>NUL
mysqld
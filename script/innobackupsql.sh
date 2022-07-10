#!/bin/bash
USER=root
PASSWORD=123456
date > /data/scripts/backup.log
echo "begin backup-------------------------------" >> /data/scripts/backup.log
find /data/mysql/backups -mtime +7 |xargs rm -rf
/usr/bin/innobackupex --defaults-file=/opt/mysql5/my.cnf --user=$USER --password=$PASSWORD --databases="test1 test2" /data/mysql/backups >> /data/scripts/backup.log 2>&1
echo "end backup-------------------------------" >> /data/scripts/backup.log
date >> /data/scripts/backup.log

mail -s "backup Passport report" "localhost@localhost" < /data/scripts/backup.log
exit 0

#!/bin/bash
USER=root
PASSWORD=123456
/etc/init.d/mysql stop
/usr/bin/innobackupex-1.5.1 --apply-log --defaults-file=/opt/mysql5/my.cnf --user=$USER --password=$PASSWORD /data/mysql/backups/passportdb/`date +%Y-%m-%d`
/usr/bin/innobackupex-1.5.1 --copy-back --defaults-file=/opt/mysql5/my.cnf --user=$USER --password=$PASSWORD /data/mysql/backups/passportdb/`date +%Y-%m-%d`
rm -rf /opt/mysql5/var/test1
rm -rf /opt/mysql5/var/test2
rm -f /opt/mysql5/var/ibdata1
rm -f /opt/mysql5/var/ib_logfile0
rm -f /opt/mysql5/var/ib_logfile1
cd /data/mysql/backups
tar zcvf `date +%Y-%m-%d`.tgz  `date +%Y-%m-%d`
rm -rf `date -d -30day +%Y-%m-%d`.tgz
cp -r /data/mysql/backups/`date +%Y-%m-%d`/ib* /opt/mysql5/var/
cp -r /data/mysql/backups/`date +%Y-%m-%d`/test1 /opt/mysql5/var/
cp -r /data/mysql/backups/`date +%Y-%m-%d`/test2 /opt/mysql5/var/
rm -rf /data/mysql/backups/`date +%Y-%m-%d`/*
chown -R mysql.mysql /opt/mysql5/var/test1
chown -R mysql.mysql /opt/mysql5/var/test2
chown mysql.mysql /opt/mysql5/var/ib*
/etc/init.d/mysql start

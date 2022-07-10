#!/bin/sh

log=/usr/local/inotify/logs/rsync.log
src="/data/img.jianke.com"
user=us
host=118.194.44.47
module=images

/usr/local/inotify/bin/inotifywait -mrq --timefmt '%d/%m/%y %H:%M' --format '%T %w %f' -e close_write,delete,create,attrib $src | while read DATE TIME DIR FILE;
        do
        FILECHANGE=${DIR}${FILE}
        /usr/bin/rsync -vzrtopg --delete --progress --password-file=/etc/rsyncd.secrets   $user@$host::$module $src &
         echo "At ${TIME} on ${DATE},file $FILECHANGE was backed up via rsync" >>$log
        done

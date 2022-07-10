#!/bin/sh
log="/var/log/rsyncd.log"
src="/data/img.jianke.com/"
host=113.105.175.73
module=images
dst="/img.jianke.com/"
/usr/local/bin/inotifywait -mrq --timefmt '%d/%m/%y %H:%M' --format '%T %w %f'  -e close_write,modify,delete,create,attrib $src | while read DATE TIME DIR FILE; do
         FILECHANGE=${DIR}${FILE}
         /usr/bin/rsync -vzrtp  --progress --delete --port=12088 $src us@$host::${module}${dst} --password-file=/etc/rsyncd.secrets &
         echo "At ${TIME} on ${DATE},file $FILECHANGE was backed up via rsync" >>$log
done

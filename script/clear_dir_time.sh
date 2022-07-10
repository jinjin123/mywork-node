#!/bin/bash
cd /srv/www/dbbackup/
find . -type d -mtime +14  -exec rm -rf {} \;

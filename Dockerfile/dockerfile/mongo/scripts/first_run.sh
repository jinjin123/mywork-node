#!/bin/bash 
USER=$MONGODB_USERNAME 
PASS=$MONGODB_PASSWORD 
DB=$MONGODB_DBNAME 
ROLE=$MONGODB_ROLE 
PRIMARY_HOST=$HOST 

# Start MongoDB service 
/usr/bin/mongod --dbpath /data --nojournal & 
while ! nc -vz localhost 27017; do sleep 1; done 

# Create User only on the Primary Pod. 
echo "Creating user: \"$USER\"..." 

a="$HOSTNAME" 
b=${a%-*-*} 

if [ ! -f /data/admin-user.lock ]; then 
  sleep 60; 
  touch /data/admin-user.lock 
  if [ "$b" = "$PRIMARY_HOST" ]; then 
    mongo $DB --eval "db.createUser({ user: '$USER', pwd: '$PASS', roles: [ { role: '$ROLE', db: '$DB' } ] });" 
  fi; 

  /usr/bin/mongod --dbpath /data --shutdown 
fi; 

/usr/bin/mongod --dbpath /data --shutdown 
echo "========================================================================" 
echo "MongoDB User: \"$USER\"" 
echo "MongoDB Database: \"$DB\"" 
echo "MongoDB Role: \"$ROLE\"" 
echo "========================================================================" 

rm -f /.firstrun 

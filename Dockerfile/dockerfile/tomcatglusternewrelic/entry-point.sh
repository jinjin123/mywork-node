#!/bin/bash

# Checking if newrelic variable is provided
if [ ! -z ${NEWRELICKEY+x} ];
then
  if [ ! -z ${NEWRELICAPPNAME+x} ];
  then
    # Applying license key and app name
    sed -i "s/  license_key: .*/  license_key: \'$NEWRELICKEY\'/" /usr/local/tomcat/newrelic/newrelic.yml
    sed -i "s/  app_name: .*/  app_name: $NEWRELICAPPNAME/" /usr/local/tomcat/newrelic/newrelic.yml
    # Installing newrelic java
    cd /usr/local/tomcat/newrelic
    chmod +x /usr/local/tomcat/newrelic/newrelic.jar
    java -jar /usr/local/tomcat/newrelic/newrelic.jar install
  fi
fi

# Check if glusterinfo is provided
if [ ! -z ${GLUSTERSERVERIP+x} ];
then
  if [ ! -z ${GLUSTERMOUNTFOLDER+x} ];
  then
    export CHECKMOUNT=`mount| grep glusterfs|grep -v grep| wc -l`
    if [ "$CHECKMOUNT" -ne "0" ];then
      mount -t glusterfs $GLUSTERSERVERIP:/glt0 $GLUSTERMOUNTFOLDER
    fi
  fi
fi

# Execute start up script
/usr/local/tomcat/bin/startup.sh >> /dev/stdout

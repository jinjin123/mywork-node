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
    CHECKLINE=`cat /usr/local/tomcat/bin/catalina.sh| grep 'javaagent:$NR_JAR'| wc -l`
    if [ "$CHECKLINE" -le "0" ];then 
      cd /usr/local/tomcat/newrelic
      chmod +x /usr/local/tomcat/newrelic/newrelic.jar
      java -jar /usr/local/tomcat/newrelic/newrelic.jar install
    fi
  fi
fi

# Execute start up script
/usr/local/tomcat/bin/startup.sh >> /dev/stdout

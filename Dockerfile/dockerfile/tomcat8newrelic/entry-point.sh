#!/bin/bash

# Checking if newrelic variable is provided
if [ ! -z ${NEWRELICKEY+x} ];
then
  if [ ! -z ${NEWRELICAPPNAME+x} ];
  then
    # Applying license key and app name
    sed -i "s/  license_key: .*/  license_key: \'$NEWRELICKEY\'/" /tomcat/newrelic/newrelic.yml
    sed -i "s/  app_name: .*/  app_name: $NEWRELICAPPNAME/" /tomcat/newrelic/newrelic.yml
    # Installing newrelic java
    cd /tomcat/newrelic
    chmod +x /tomcat/newrelic/newrelic.jar
    java -jar /tomcat/newrelic/newrelic.jar install
  fi
fi

/tomcat/bin/catalina.sh start && tail -f /tomcat/logs/catalina.out >> /dev/stdout

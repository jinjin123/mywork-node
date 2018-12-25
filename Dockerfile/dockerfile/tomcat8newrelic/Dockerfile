FROM docker.io/cloudesire/tomcat:8-jre8

RUN mkdir -p /data

RUN apt-get update
RUN apt-get -y install apt-transport-https
RUN apt-get -y install unzip

# Install new relic with a given key (todo: make it dynamic)
WORKDIR /tomcat
ADD ./newrelic.zip newrelic.zip
RUN unzip newrelic.zip
WORKDIR /tomcat/newrelic
ADD ./entry-point.sh /root/entry-point.sh
RUN chmod +x /root/entry-point.sh
ENTRYPOINT ["/root/entry-point.sh"]
WORKDIR /tomcat/webapps

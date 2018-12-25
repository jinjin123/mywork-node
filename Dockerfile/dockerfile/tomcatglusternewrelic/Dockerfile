FROM tomcat:7.0.78-jre7

RUN mkdir -p /data

RUN apt-get update
RUN apt-get -y install apt-transport-https

RUN wget -O - http://download.gluster.org/pub/gluster/glusterfs/3.7/3.7.9/rsa.pub | apt-key add -

RUN echo deb http://download.gluster.org/pub/gluster/glusterfs/3.7/3.7.9/Debian/jessie/apt jessie main > /etc/apt/sources.list.d/gluster.list

RUN apt-get update
RUN apt-get -y install glusterfs-client

# Install new relic with a given key (todo: make it dynamic)
WORKDIR /usr/local/tomcat
ADD ./newrelic.zip newrelic.zip
RUN unzip newrelic.zip
WORKDIR /usr/local/tomcat/newrelic
ADD ./entry-point.sh /root/entry-point.sh
ENTRYPOINT ["/root/entry-point.sh"]
WORKDIR /usr/local/tomcat/webapps

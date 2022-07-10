FROM tomcat:7.0.78

RUN apt-get update
RUN apt-get -y install apt-transport-https
RUN wget -O - http://download.gluster.org/pub/gluster/glusterfs/3.7/3.7.9/rsa.pub | apt-key add -
RUN echo deb http://download.gluster.org/pub/gluster/glusterfs/3.7/3.7.9/Debian/jessie/apt jessie main > /etc/apt/sources.list.d/gluster.list
RUN apt-get update
RUN apt-get -y install glusterfs-client
RUN apt-get -y install openjdk-7-jdk

ENV NEWRELICKEY 7b594fa2067ea81aa489d399aab50b5385b27624
ENV NEWRELICAPPNAME KYBOT_QA
ENV GLUSTERSERVERIP 10.0.0.61
ENV GLUSTERMOUNTFOLDER /data

# Install new relic with a given key (todo: make it dynamic)
WORKDIR /usr/local/tomcat
ADD ./newrelic.zip newrelic.zip
RUN unzip newrelic.zip
WORKDIR /usr/local/tomcat/newrelic
ADD ./entry-point.sh /root/entry-point.sh
RUN chmod +x /root/entry-point.sh
RUN ["sh", "-c", "/root/entry-point.sh"]
# Try to restart tomcat
RUN /usr/local/tomcat/bin/catalina.sh stop 10 -force && /usr/local/tomcat/bin/catalina.sh start
WORKDIR /usr/local/tomcat/webapps

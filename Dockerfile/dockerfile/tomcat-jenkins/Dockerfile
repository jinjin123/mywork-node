FROM docker.io/milcom/centos7-systemd
RUN set -x && \
    echo y | yum install -y wget  \
    gcc \
    cyrus-sasl-devel \
    unzip \
    wget \
    gcc-c++ \
    autoconf \
    automake \
    libtool \
    make \
    cmake \
    openssl \
    openssl-devel \
    openssh-* \
    java \
    net-tools \
    epel-release \
    python-setuptools \
    ansible

##enable ssh
RUN set -x && \
    sed -i '#PermitRootLogin yes/PermitRootLogin yes' /etc/ssh/sshd_config

### install jenkins
RUN set -x && \
    mkdir -p /opt/jenkins && \
    cd /opt/jenkins && \
    wget http://123.207.123.231/packages/apache-tomcat-8.0.36.tar.gz && \
    tar  -xvf  apache-tomcat-8.0.36.tar.gz &&  \
    cd /opt/jenkins/apache-tomcat-8.0.36/webapps && \
    rm -rf ROOT && \
    wget http://123.207.123.231/packages/jenkins.war && \
    mv jenkins.war ROOT.war

#install supervisor
#RUN set -x && \
#    easy_install supervisor && \
#    mkdir -p /var/{log/supervisor,run/{sshd,supervisord}}

# chaning timezone
RUN  set -x && \
    unlink /etc/localtime && \
    ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# chaning passwd
RUN echo 'jinjin123' | passwd --stdin root


EXPOSE 8080


# Insert supervisord conf file
#ADD supervisord.conf /etc/

#start
#ADD startup.sh /var/www/startup.sh
#RUN chmod +x /var/www/startup.sh

#start it
#ENTRYPOINT ["/var/www/startup.sh"]
ENTRYPOINT /opt/jenkins/apache-tomcat-8.0.36/bin/startup.sh && tail -f /opt/jenkins/apache-tomcat-8.0.36/logs/catalina.out

#setting working directory
WORKDIR /root/.jenkins/workspace

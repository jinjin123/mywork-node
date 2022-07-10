FROM centos:7
#PROJECT Fourtune
#ENV apache 2.4.6 php5.4.16 mysql5.5

RUN set -x && \
    yum install -y gcc \
    cyrus-sasl-devel \
    unzip \
    wget \
    gcc-c++ \
    autoconf \
    automake \
    libtool \
    make \
    cmake

RUN set -x && \
    rpm -ivh http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm && \
    yum install -y zlib  \
    zlib-devel  \
    re2c   \
    openssl \
    openssl-devel \
    pcre-devel \
    libxml2  \
    libxml2-devel \
    libcurl   \
    libcurl-devel \
    libpng-devel \
    libjpeg-devel \
    freetype-devel \
    libmcrypt-devel \
    openssh-server \
    python-setuptools \
    libxslt-devel*  \
    libmcrypt  \
    mysql

RUN set -x && \
    yum install -y httpd \
    php-fpm \
    php \
    mcrypt \
    mhash \
    php-pear

#Install supervisor
RUN set -x && \
    easy_install supervisor && \
    mkdir -p /var/{log/supervisor,run/{sshd,supervisord}}

RUN yum list installed|grep mcrypt

RUN yum clean all
RUN yum remove -y epel-release

RUN /usr/bin/pecl channel-update pecl.php.net

RUN yum install  -y epel-release
RUN set -x  && \
    yum install -y php-mcrypt \
    php-xsl \
    #xdebug-2.6.0 \
    xdebug  \
    php-mysqli \
    php-pdo

RUN mkdir -p /var/www/logs
RUN chmod 777 -R  /var/www/logs

ADD httpd.conf /etc/httpd/httpd.conf
ADD vhost.conf /etc/httpd/conf.d/vhost.conf
ADD index.php /var/www/html
ADD supervisord.conf /etc/
ADD startup.sh /var/www/startup.sh
RUN chmod +x /var/www/startup.sh

EXPOSE 80 443
#Start it
ENTRYPOINT ["/var/www/startup.sh"]

WORKDIR /var/www/html

FROM centos:7
RUN yum install -y openssh-server
RUN yum install -y openssh-*
RUN yum install -y openssl
ADD run.sh /run.sh
RUN chmod 777 /run.sh
RUN mkdir /data
ADD ssh_host_rsa_key /etc/ssh/ssh_host_rsa_key
RUN chmod 600 /etc/ssh/ssh_host_rsa_key
RUN echo "root:zxc!@#^" |chpasswd

WORKDIR  /
CMD ["./run.sh"]

FROM centos:7
RUN set -x && \
    yum install  -y vsftpd  \
    ftp \
    openssh-server \ 
    openssh-* \
    openssl \
    epel-release  \
    openssl \
    openssl-devel \
    net-tools 

RUN set -x && \
    yum install -y supervisor

ADD startup.sh /startup.sh
RUN chmod +x /startup.sh


ADD requirements.txt /etc/
#RUN pip3 install -r  /etc/requirements.txt

RUN mkdir -p /var/{log/supervior,log/gunicorn,run/supervisord}
RUN mkdir  -p /usr/local/
ADD jdk1.8.0_231-amd64 /usr/local/jdk1.8.0_231-amd64
ADD supervisord.conf /etc/


ADD profile /etc/profile

RUN touch /root/.bashrc
RUN touch /root/.bash_profile

RUN echo "source /etc/profile" >> /root/.bashrc

#ADD ssh_host_rsa_key /etc/ssh/ssh_root_rsa_key
#ADD ssh_host_ecdsa_key /etc/ssh/ssh_host_ecdsa_key
#ADD ssh_host_ed25519_key /etc/ssh/ssh_host_ed25519_key


#ADD run.sh /run.sh
#RUN chmod 777 /run.sh
WORKDIR  /root/
#ENTRYPOINT ["/run.sh"]
#CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
ENTRYPOINT ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisord.conf"] 



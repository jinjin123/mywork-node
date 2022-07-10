FROM mongo:5.0.6 

ENV DEBIAN_FRONTEND noninteractive 
ENV DEBCONF_NONINTERACTIVE_SEEN true 

RUN apt-get -qqy update \ 
&& apt-get -qqy upgrade \ 
&& apt-get -qqy install -y netcat \ 
&& apt-get -qqy install rsyslog 

# Add scripts 
ADD scripts /scripts 
RUN chmod +x /scripts/*.sh 
RUN touch /.firstrun 

RUN (crontab -l ; echo "0 0 * * * bash /scripts/logs.sh") | crontab 

# Command to run 
ENTRYPOINT ["/scripts/run.sh"] 

# Expose listen port 
EXPOSE 27017 
EXPOSE 28017 

# Expose our data volumes 
VOLUME ["/data"] 

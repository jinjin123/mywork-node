from dockerpriv.shadowdock.com/keithyau/logstash                                                                                                                                            
COPY docker-entrypoint.sh /usr/local/proxy/docker-entrypoint.sh                                                                                                                             
RUN chmod a+x /usr/local/proxy/docker-entrypoint.sh                                                                                                                                         
COPY logstash.conf /opt/logstash/conf/logstash.conf                                                                                                                                         
EXPOSE 5000                                                                                                                                                                                 
EXPOSE 5044                                                                                                                                                                                 
ENTRYPOINT ["/usr/local/proxy/docker-entrypoint.sh" , "> /dev/stdout"] 

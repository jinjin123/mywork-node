FROM  hub.c.163.com/zhexuezhenhanzi/rabbitmq:latest

ADD setup  /setup
ADD rabbitmq.config /etc/rabbitmq/rabbitmq.config
ADD enabled_plugins  /etc/rabbitmq/enabled_plugins
RUN rm /etc/localtime
RUN ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN chmod a+x /setup

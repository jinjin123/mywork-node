FROM ubuntu:latest
RUN apt-get update
RUN echo "y" | apt-get install libjpeg8-dev zlib1g-dev  libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk
RUN echo "y" | apt-get install python-pip
RUN pip install pip --upgrade  -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
RUN pip install websocket  -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
RUN pip install websocket-client  -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
RUN pip install pillow -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
RUN pip install python-escpos  -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
RUN echo "y" | apt-get install usbutils

RUN which python
RUN mkdir -p /usr/local/proxy
ADD printer /usr/local/proxy/printer
COPY docker-entrypoint.sh /usr/local/proxy/docker-entrypoint.sh
RUN chmod a+x /usr/local/proxy/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/proxy/docker-entrypoint.sh", "> /dev/stdout"]
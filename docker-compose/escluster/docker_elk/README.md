SparkPad Logging

yum install bash-completion

安装Docker

curl -sSL http://acs-public-mirror.oss-cn-hangzhou.aliyuncs.com/docker-engine/internet | sh -
systemctl enable docker
systemctl start docker

安装Docker-compose

curl -L https://github.com/docker/compose/releases/download/1.11.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

bash 补全
curl -L https://raw.githubusercontent.com/docker/compose/1.11.2/contrib/completion/bash/docker-compose > /etc/bash_completion.d/docker-compose

/etc/sysctl.conf配置max_map_count
vm.max_map_count=262144

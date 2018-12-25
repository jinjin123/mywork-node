
#真功夫服务器docker安装
```bash
cd /etc/yum.repos.d/
mv CentOS-VSFTP.repo CentOS-VSFTP.repo.bak
mv CentOS-Base.repo.bak CentOS-Base.repo
yum update
```
* 安装docker

> [centos安装docker](https://docs.docker.com/engine/installation/linux/centos/) 或者 [daocloud](https://get.daocloud.io/#install-docker)

* 安装docker-compose

> [daocloud](https://get.daocloud.io/#install-compose)

* docker初始化及网络配置

> systemctl enable docker.service ##开机自启动

> sudo usermod -aG docker spark

* 配置网络： 

> touch /etc/sysconfig/network-scripts/ifcfg-br0
> 
<pre>
TYPE=Bridge
BOOTPROTO=static
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
#IPV6INIT=yes
#IPV6_AUTOCONF=yes
#IPV6_DEFROUTE=yes
#IPV6_FAILURE_FATAL=no
NAME=bridge0
DEVICE=bridge0
ONBOOT=yes
IPADDR=10.255.254.1
PREFIX=24
</pre>

* 创建docker运行配置

<pre>
#停止docker服务器，并删除docker0网卡。如果没有可以不执行。
sudo systemctl stop docker
sudo ip link set dev docker0 down
sudo brctl delbr docker0
 
# 创建自定义bridge0网络，网段为10.255.254.1/24。如果已经存在可以不用执行。
sudo brctl addbr bridge0
sudo ip addr add 10.255.254.1/24 dev bridge0
sudo ip link set dev bridge0 up
#sudo ip link set dev bridge0 down ; sudo brctl delbr bridge0
 
# 确认网卡已经运行
ip addr show bridge0
 
# 创建docker运行的配置文件（如果文件夹不存在，手工创建）
sudo mkdir /etc/systemd/system/docker.service.d
sudo vi /etc/systemd/system/docker.service.d/docker.conf##输入如下内容
 
[Service]
EnvironmentFile=-/etc/sysconfig/docker
ExecStart=
ExecStart=/usr/bin/dockerd $OPTIONS \
          $DOCKER_STORAGE_OPTIONS \
          $DOCKER_NETWORK_OPTIONS \
          $BLOCK_REGISTRY \
          $INSECURE_REGISTRY
           
# 修改docker服务启动默认绑定网卡为bridge0
echo 'DOCKER_NETWORK_OPTIONS="-b=bridge0"' >> /etc/sysconfig/docker
 
sudo systemctl daemon-reload
 
sudo systemctl restart docker

</pre>
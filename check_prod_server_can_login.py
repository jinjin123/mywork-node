#!/usr/bin/env python
# -*- coding: utf-8 -*
import paramiko, re,socket,requests
import os,sys,json,time,subprocess
reload(sys)
sys.setdefaultencoding("utf-8")
class SSH_SSH(object):
    def __init__(self):
        self.base_prompt = r'(>|#|\]|\$|\)) *$'
        self.active = False
        self.prompt = ""

    def login(self, **kws):
        ssh_info = {"status": False, "content": ""}
        try:
            self.username = kws["user"]
            self.password = kws["pwd"]
            self.port = kws["port"]
            self.lg_type = kws["lg_type"]
            self.ip = kws["ip"]
            self.keyfile = kws["keyfile"]
            self.port = int(self.port)
            ssh = paramiko.SSHClient()
            if str(self.lg_type) == str("密码方式"):
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.ip, self.port, self.username, self.password)
            else:
                key = paramiko.RSAKey.from_private_key_file(self.keyfile)
                ssh.load_system_host_keys()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.ip, self.port, self.username, pkey=key)
            self.channel = ssh
            self.shell = ssh.invoke_shell(width=1000, height=1000)
            self.active = True
            data = self.clean_buffer()
            if not data["status"]: raise SSHError(data["content"])
            data = self.get_prompt()  # 换成设置统一prompt
            if not data["status"]:
                raise SSHError(data["content"])
            else:
                ssh_info["content"] = data["content"]
            ssh_info["status"] = True
        except KeyError, e:
            ssh_info["content"] = "缺少字段 %s" % str(e)
        except socket.error:
            ssh_info["content"] = "无法连接端口"
        except socket.gaierror:
            ssh_info["content"] = "无法联系上这个主机"
        except paramiko.ssh_exception.AuthenticationException:
            ssh_info["content"] = "账号或者密码错误"
        except paramiko.ssh_exception.BadAuthenticationType:
            if lg_type == 'key':
                ssh_info["content"] = "认证类型应该是密码"
            else:
                ssh_info["content"] = "认证类型应该是秘钥"
        except Exception, e:
            print str(e)
            ssh_info['status'] = False
            ssh_info['content'] = str(e)
        if re.search("not a valid RSA private key file", ssh_info["content"]):
            ssh_info["content"] = "无效的秘钥文件"
        return ssh_info

    def get_prompt(self):
        buff = ''
        ssh_info = {"status": False, "content": ""}
        try:
            self.shell.send('\n')
            while not re.search(self.base_prompt, buff.split('\n')[-1]):
                buff += self.shell.recv(1024)
            ssh_info["content"] = buff
            self.prompt = re.escape(buff.split('\n')[-1])
            ssh_info["status"] = True
        except Exception, e:
            ssh_info["content"] = "获取主机提示符错误:[%s]" % str(e)
            ssh_info["status"] = False
        return ssh_info

    def clean_buffer(self):
        ssh_info = {"status": False, "content": ""}
        try:
            if not self.active: raise SSHError("已经与主机断开连接")
            self.shell.send('\n')
            time.sleep(0.5)
            buff = ""
            while not re.search(self.prompt.split('\r\n')[-1], buff):
                buff += self.shell.recv(512)
            ssh_info["status"] = True
        except Exception, e:
            print "清除缓存失败", str(e)
            ssh_info["status"] = False
            ssh_info["content"] = str(e)
        return ssh_info

if __name__ == "__main__":
    server = {"user": "yau","pwd": '',"port":22,"lg_type": "秘钥方式","ip": "54.178.240.198","keyfile": "/home/yau/keys/cloud"}
    ssh=SSH_SSH()
    data=ssh.login(**server)
    data["time"]=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    if data["status"]:
        #data["status"]="login success"
        #data["info"]="login success, keepalive  heartbeat"
        pass
    else:
        data["status"]="login failed"
	data["info"]="login faild,trying restart server"
        cmd = "echo 'prod' | sh /root/api_reboot_shanghai"
        cmd_status = subprocess.Popen(cmd, shell=True, executable='/bin/bash')
        data["restart_info"]=cmd_status
        res = requests.post("http://182.254.154.81:8080/notify",data=json.dumps(data))

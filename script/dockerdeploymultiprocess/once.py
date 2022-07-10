import os
import paramiko

# paramiko.util.log_to_file("/tmp/paramiko.log")
filepath = os.path.split(os.path.realpath(__file__))[0]


class Conn:
    def __init__(self, ip, port=22, username='ops'):
        self.ip = ip
        self.port = int(port)
        self.username = username

        self.pkey = paramiko.RSAKey.from_private_key_file(
            filepath + '/ssh_private.key'
        )

    def cmd(self, cmd):
        ssh = paramiko.SSHClient()

        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip, self.port, self.username, pkey=self.pkey, timeout=5)
        except Exception as err:
            data = {"state": 0, "message": str(err)}
        else:
            try:
                stdin, stdout, stderr = ssh.exec_command(cmd, timeout=180)
                _err_list = stderr.readlines()

                if len(_err_list) > 0:
                    data = {"state": 0, "message": _err_list}
                else:
                    data = {"state": 1, "message": stdout.readlines()}
            except Exception as err:
                data = {"state": 0, "message": '%s: %s' % (self.ip, str(err))}
        finally:
            ssh.close()

        return data


if __name__ == '__main__':
    # 演示代码简化了很多，整体逻辑不变

    hostlist = ['10.82.9.47', '10.82.9.48']
    image_url = 'ops-coffee:latest'

    for i in hostlist:
        print(Conn(i).cmd('docker pull %s' % image_url))
        # 在镜像下载完成后进行更新容器的操作，代码类似省略了

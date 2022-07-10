import threading
from math import ceil
# 再导入上一个示例里边的Conn类

class DeployThread(threading.Thread):
    def __init__(self, thread_max_num, host, project_name, environment_name, image_url):
        threading.Thread.__init__(self)
        self.thread_max_num = thread_max_num
        self.host = host
        self.project_name = project_name
        self.environment_name = environment_name
        self.image_url = image_url

    def run(self):
        self.smile_host = []
        with self.thread_max_num:
            Conn(self.host).cmd('docker stop %s && docker rm %s' % (self.project_name, self.project_name))

            r5 = Conn(self.host).cmd(
                'docker run -d --env ENVT=%s --env PROJ=%s --restart=always --name=%s -p 80:80 %s' % (
                    self.environment_name, self.project_name, self.project_name, self.image_url)
            )

            if r5.get('state'):
                self.smile_host.append(self.host)
                print('---->%s镜像更新完成' % (self.host))
            else:
                print('---->%s服务器执行docker run命令失败,details:%s' % (self.host, r5.get('message')))

            # check镜像重启状态 and 重启失败需要回滚代码省略

    def get_result(self):
        return self.smile_host


if __name__ == '__main__':
    # 演示代码简化了很多，整体逻辑不变

    alive_host = ['10.82.9.47', '10.82.9.48']
    image_url = 'ops-coffee:latest'

    project_name = 'coffee'
    environment_name = 'prod'

    # alive_host / 8 向上取整作为最大线程数
    thread_max_num = threading.Semaphore(ceil(len(alive_host) / 8))

    threads = []
    for host in alive_host:
        t = DeployThread(thread_max_num, host, project_name, environment_name, image_url)
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    smile_host = []
    for t in threads:
        smile_host.append(t.get_result())

    print('---->%d台主机更新成功' % (len(smile_host)))

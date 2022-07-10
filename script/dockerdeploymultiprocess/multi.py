import threading
# 再导入上一个示例里边的Conn类

class DownloadThread(threading.Thread):

    def __init__(self, host, image_url):
        threading.Thread.__init__(self)
        self.host = host
        self.image_url = image_url

    def run(self):
        Conn(self.host).cmd('docker login -u ops -p coffee hub.ops-coffee.cn')
        r2 = Conn(self.host).cmd('docker pull %s' % self.image_url)
        if r2.get('state'):
            self.alive_host = self.host
            print('---->%s镜像下载完成' % self.host)
        else:
            self.alive_host = None
            print('---->%s镜像下载失败，details：%s' % (self.host, r2.get('message')))

    def get_result(self):
        return self.alive_host


if __name__ == '__main__':
    # 演示代码简化了很多，整体逻辑不变

    hostlist = ['10.82.9.47', '10.82.9.48']
    image_url = 'ops-coffee:latest'

    threads = []
    for host in hostlist:
        t = DownloadThread(host, image_url)
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    alive_host = []
    for t in threads:
        alive_host.append(t.get_result())
    ## 多线程下载镜像结束

    print('---->本项目共有主机%d台，%d台主机下载镜像成功' % (len(hostlist), len(alive_host)))

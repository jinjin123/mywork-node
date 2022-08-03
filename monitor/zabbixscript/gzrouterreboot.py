#!/usr/local/python3/bin/python3
#guanzhou router reboot
import socket,urllib.request,base64,http.cookiejar

ip = "218.107.9.124"
user = "admin"
passwd = "jiankecom"

class MyHttp:
    def __init__(self, timeout=10, addHeaders=True):
        socket.setdefaulttimeout(timeout)   # 设置超时时间

        self.__opener = urllib.request.build_opener()
        urllib.request.install_opener(self.__opener)

        if addHeaders: self.__addHeaders()

    def __error(self, e):
        '''错误处理'''
        print(e)

    def __addHeaders(self):
        '''添加默认的 headers.'''
        self.__opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'),\
                                ('Connection', 'keep-alive'),\
                                ('Cache-Control', 'no-cache'),\
                                ('Accept-Language:', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'),\
                                ('Accept-Encoding', 'gzip, deflate'),\
                                ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]

    def __decode(self, webPage, charset):
        '''gzip解压，并根据指定的编码解码网页'''
        if webPage.startswith(b'\x1f\x8b'):
            return gzip.decompress(webPage).decode(charset)
        else:
            return webPage.decode(charset)

    def addCookiejar(self):
        '''为 self.__opener 添加 cookiejar handler。'''
        cj = http.cookiejar.CookieJar()
        self.__opener.add_handler(urllib.request.HTTPCookieProcessor(cj))

    def get(self, url, params={}, headers={}, charset='GBK'):  
        '''''HTTP GET 方法'''  
        if params: url += '?' + urllib.parse.urlencode(params)  
        request = urllib.request.Request(url)  
        for k,v in headers.items(): request.add_header(k, v)    # 为特定的 request 添加指定的 headers  
        try:  
            response = urllib.request.urlopen(request)  
        except urllib.error.HTTPError as e:  
            self.__error(e)  
        else:  
            return self.__decode(response.read(), charset)  
        
    def post(self, url, params={}, headers={}, charset='GBK'):
        params = urllib.parse.urlencode(params)
        request = urllib.request.Request(url, data=params.encode(charset))
        for k,v in headers.items(): request.add_header(k, v)

        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            self.__error(e)
        else:
            return self.__decode(response.read(), charset)

if __name__ == "__main__":
    ht = MyHttp()
    ht.addCookiejar()
    user = str(base64.b64encode(bytes(user,'utf8')),'utf8')
    passwd = str(base64.b64encode(bytes(passwd,'utf8')),'utf8')
    url = "https://" + ip + "/cgi-bin/wlogin.cgi"
    ht.post(url,params={'aa':user, 'ab':passwd})
    url = "https://" + ip + "/cgi-bin/reboot.cgi"
    ht.post(url,params={'sReboot':'Current', 'submit':'È·¶¨'})


# coding=utf-8
from time import sleep
from selenium import webdriver

class RemoteBrowser:

    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('whitelisted-ips')
    #chrome_options.add_argument('headless')
    chrome_options.add_argument('no-sandbox')
    #chrome_options.add_argument('window-size=1200x800')

    def __init__(self):
        #self.hub_url = os.environ['HUB_URL']
        self.hub_url = "http://localhost:9515/wd/hub"
        self.driver = webdriver.Remote(
            command_executor=self.hub_url,
            #desired_capabilities = {'browserName': 'chrome'},
            options=self.chrome_options
        )

    def getobj(self):
        title = self.driver.get("https://www.baidu.com")
        print(title)



#browser = webdriver.Remote("http://localhost:9515/wd/hub", chrome_options=chrome_options)
#browser.get("http://www.163.com")

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('--user-data-dir=/home/seluser/data')
# for server, local debug not need
#chromeOptions.add_argument('--disable-dev-shm-usage')
#chromeOptions.add_argument('--no-sandbox')
#chromeOptions.add_argument('--headless')
chromeOptions.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
#driver = webdriver.Remote(command_executor='http://192.168.1.110:9515/wd/hub',
                          options=chromeOptions)

#driver.get("https://www.baidu.com")
driver.get("https://jlpt.neea.edu.cn/index.do")
#driver.execute("addScriptToEvaluateOnNewDocument",{
#          "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
#        })
print(driver.title)
#driver.quit()
sleep(60)
driver.quit()

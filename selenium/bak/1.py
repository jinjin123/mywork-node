# coding=utf-8
from time import sleep
from selenium import webdriver



#browser = webdriver.Remote("http://localhost:9515/wd/hub", chrome_options=chrome_options)
#browser.get("http://www.163.com")

chromeOptions = webdriver.ChromeOptions()
#chromeOptions.add_argument('--user-data-dir=/home/seluser/data')
# for server, local debug not need
#chromeOptions.add_argument('--disable-dev-shm-usage')
#chromeOptions.add_argument('--no-sandbox')
#chromeOptions.add_argument('--headless')
chromeOptions.add_argument("--disable-blink-features=AutomationControlled")
chromeOptions.add_experimental_option('excludeSwitches',['enable-automation'])
driver=webdriver.Chrome(executable_path="/home/jin/project/dotnet/ex/bin/release/net6.0/chromedriver",options=chromeOptions)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
          "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
driver.get("https://jlpt.neea.edu.cn/index.do")


#driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
#driver = webdriver.Remote(command_executor='http://192.168.1.110:9515/wd/hub',
#                          options=chromeOptions)

#driver.get("https://www.baidu.com")
#driver.get("https://jlpt.neea.edu.cn/index.do")
#driver.execute("addScriptToEvaluateOnNewDocument",{
#          "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
#        })
#print(driver.title)
#driver.quit()
#sleep(60)
#driver.quit()

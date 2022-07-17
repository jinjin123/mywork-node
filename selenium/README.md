```

#网上最常见的处理方式如下,原理就是在每次新页面加载之前执行JS通过Chrome Devtools-ProtocolAPI去删除window.navigator.webdriver属性.

from selenium.webdriver import Chrome
 
driver = Chrome('./chromedriver')
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
driver.get('https://www.kagura.me')
#但是,如果是调用远程webdriver时则会报错:AttributeError: 'WebDriver' object has no attribute 'execute_cdp_cmd'


from selenium import webdriver
 
driver = webdriver.Remote(command_executor="http://127.0.0.1:4444/wd/hub")
# 会报错 AttributeError: 'WebDriver' object has no attribute 'execute_cdp_cmd'
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
driver.get('https://www.kagura.me')
#其实在远程调用的情况下,使用--disable-blink-features=AutomationControlled 参数即可完美去除window.navigator.webdriver,完整代码如下:

from selenium import webdriver
 
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Remote(command_executor="http://127.0.0.1:4444/wd/hub", options=options)
driver.get('https://www.kagura.me')
```

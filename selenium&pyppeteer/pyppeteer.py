import pyppeteer
import asyncio
from pyppeteer import launch
import requests
import os
import random
from pyppeteer.dialog import Dialog
from pyppeteer.network_manager import  Response


async def run(numid: str, numpwd: str, level: int, school_id: int, school_name: str, remote_port: int, data_num: int):
    # address = 'ws://127.0.0.1:9222/devtools/browser/5fe6ee78-3f36-4294-b904-fc7e9d8c2119'
    # browser = await pyppeteer.launcher.connect({'browserWSEndpoint': address})

    ## open with remote port chrome
    os.popen(
    "/home/jin/.local/share/pyppeteer/local-chromium/588429/chrome-linux/chrome "
    "--remote-debugging-port=%d --no-first-run --no-default-browser-check --user-data-dir=./test-%d"%(remote_port,data_num))
    # os.popen(
    #     "/usr/bin/google-chrome-stable "
    #     "--remote-debugging-port=%d --no-first-run --no-default-browser-check --user-data-dir=./test-%d"%(remote_port,data_num))
    await asyncio.sleep(3)
    debug_blank_page = requests.get("http://127.0.0.1:9222/json/version", headers={"Content-Type": "application/json"})
    wslink = (debug_blank_page.json())["webSocketDebuggerUrl"]
    browser = await pyppeteer.launcher.connect({'browserWSEndpoint': wslink})

    # browser = await launch(headless=False,executablePath="/home/jin/.local/share/pyppeteer/local-chromium/588429/chrome-linux/chrome",ignoreDefaultArgs=['--enable-automation'])  # 关闭无头浏览器
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080})
    await page.goto('https://jlpt.neea.edu.cn/index.do', options={'timeout': 10000})
    # sleep(1)
    # wait for render
    await page.waitForNavigation()
    try:
        user = await page.querySelector("#loginForm > table > tbody > tr:nth-child(2) > td:nth-child(2) > input[type=text]")
        if user is not None:
            await user.type(numid)
            pwd = await page.querySelector(
                "#loginForm > table > tbody > tr:nth-child(4) > td:nth-child(2) > input[type=password]")
            await pwd.type(numpwd)
            # show img
            await page.evaluate(pageFunction='''() => {
                showChkImg();
            }''', force_expr=False)
            # loop untill login success
            while True:
                code = input("code ->")
                print(code)
                if code == "":
                    # enter refresh check code
                    await page.evaluate(pageFunction='''() => {
                         showChkImg();
                        getChkimgAjax('loginDiv');
                    }''', force_expr=False)
                    continue
                elif code == 'a':
                    await page.evaluate(pageFunction='''() => {
                        selectedJB(%d)
                    }'''% level , force_expr=False)
                    # inside window check code & loop until submit
                    while True:
                        sub_code = input("sub_code->")
                        if sub_code == "":
                            # refresh
                            await page.evaluate(pageFunction='''() => {
                                getChkimgAjax('chooseaddrDiv');
                            }''', force_expr=False)
                            continue
                        else:
                            sub_co = await page.querySelector('#chooseaddrForm > table:nth-child(1) > tbody > tr:nth-child(2) > td.inputChk > input[type="text"]:nth-child(2)')
                            await sub_co.type(sub_code)
                            await page.evaluate(pageFunction='''() => {
                                bookseat('chooseaddrForm',%d,'%s')
                            }'''%(school_id,school_name) , force_expr=False)
                            await page.waitForNavigation()
                            # not working
                            #await page.keyboard.press('Enter')
                            continue
                else:
                    co = await page.querySelector(
                        "#loginForm > table > tbody > tr:nth-child(6) > td:nth-child(2) > input[type=text]")
                    await co.type(code)
                    await page.click("#btnlogin")
                    # not working
                    # await page.setRequestInterception(True)
                    #Dont forget the lambda it make the page.on calling whatever function you want
                    # page.on('response', interceptResponse)
                    # page.on(
                    #     'dialog',
                    #     lambda dialog: asyncio.ensure_future(close_dialog(dialog))
                    # )
                    # break

    except Exception as e:
        print(e)
    # asyncio.get_event_loop().run_until_complete(run(numid, numpwd, level, school_id, school_name,remote_port,data_num))

async def interceptResponse(res):
    print(res)
    if (res.url).startswith("https://jlpt.neea.edu.cn/login.do"):
        content = res.json()
        print(content)

async def booking(page,level,school_id,school_name):
    # wait for loading
    # await asyncio.sleep(3)
    await page.evaluate(pageFunction='''() => {
        selectedJB(%d)
    }''' % (level), force_expr=False)
    await asyncio.sleep(3)
    await page.evaluate(pageFunction='''() => {
        bookseat('chooseaddrForm',%d,'%s')
    }''' % (school_id, school_name), force_expr=False)
    await asyncio.sleep(30)


async def close_dialog(dialog: Dialog):
    """
        page.on("dialog", get_content)
    :param dialog:
    :return:
    """
    await dialog.dismiss()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run('id', 'pwd', 2, 3, '北京语言大学',9222 ,random.randint(1,100)))

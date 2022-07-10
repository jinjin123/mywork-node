#!/usr/bin/python
import os
import pymysql
import requests
import boto3
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

db= pymysql.connect(host='10.0.0.30',port=3306,user='root', passwd='root', db='spiderflowbak',charset='utf8')
cursor = db.cursor()

cursor.execute("select detailUrl from watch2 where id > 2257 and id <= 30000")
data = [i[0] for i in cursor.fetchall()]

s3 = boto3.resource('s3')
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36'}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")
driver = os.path.join("/usr/bin","chromedriver")
browser = webdriver.Chrome(executable_path=driver,chrome_options=chrome_options)
style = browser.find_elements_by_css_selector(".flexslider-thumbnails>div[style]")
for ul in data:
  img = []
  browser.get("https://www.chrono24.com/" +ul)
  style = browser.find_elements_by_css_selector(".flexslider-thumbnails>div[style]")
  for x in style:
     b = (x.get_attribute("style")).split("(")[1].split(")")[0].replace('"','')
     if b.find("images_") != -1:
        source = b.replace("s140","xxl")
        res=requests.get(source,headers=headers)
        imgname = source.split("uhren/")[1]
        #s3 url save to db
	url="https://wristcheck.s3.ap-east-1.amazonaws.com/detailImg/"+ imgname
        img.append(url)
        s3.Bucket('wristcheck').put_object(Key="detailImg/"+imgname, Body=res.content)
     elif b.find("Square140") != -1:
        source = b.replace("Square140","ExtraLarge")
        res=requests.get(source,headers=headers)
        imgname = source.split("uhren/")[1]
	#s3 url save to db
	url="https://wristcheck.s3.ap-east-1.amazonaws.com/detailImg/"+ imgname
	img.append(url)
	s3.Bucket('wristcheck').put_object(Key="detailImg/"+imgname, Body=res.content)

  l="""update watch2 set detailimg = ("%s") where detailUrl = ("%s")""" % (img,ul)
  b="""insert into log  (detailUrl) values ("%s") """ % (ul)
  try:
    cursor.execute(l)
    cursor.execute(b)
    db.commit()
  except:
    pass
  time.sleep(1)

browser.close()


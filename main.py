import MySQLdb
import time
import sys
import re
from datetime import date, timedelta,datetime
from bs4 import BeautifulSoup
from selenium import webdriver

weburl = sys.argv[1]
anvato_id = sys.argv[2]

conn = MySQLdb.connect(host="localhost",user="", passwd="", db="linetoday", charset="utf8")

regex1 = re.compile(r'\d+/\d+/\d+')

option = webdriver.ChromeOptions()
lambda_options = [
    '--autoplay-policy=user-gesture-required',
    '--disable-background-networking',
    '--disable-background-timer-throttling',
    '--disable-backgrounding-occluded-windows',
    '--disable-breakpad',
    '--disable-client-side-phishing-detection',
    '--disable-component-update',
    '--disable-default-apps',
    '--disable-dev-shm-usage',
    '--disable-domain-reliability',
    '--disable-extensions',
    '--disable-features=AudioServiceOutOfProcess',
    '--disable-hang-monitor',
    '--disable-ipc-flooding-protection',
    '--disable-notifications',
    '--disable-offer-store-unmasked-wallet-cards',
    '--disable-popup-blocking',
    '--disable-print-preview',
    '--disable-prompt-on-repost',
    '--disable-renderer-backgrounding',
    '--disable-setuid-sandbox',
    '--disable-speech-api',
    '--disable-sync',
    '--disk-cache-size=33554432',
    '--hide-scrollbars',
    '--ignore-gpu-blacklist',
    '--ignore-certificate-errors',
    '--metrics-recording-only',
    '--mute-audio',
    '--no-default-browser-check',
    '--no-first-run',
    '--no-pings',
    '--no-sandbox',
    '--no-zygote',
    '--password-store=basic',
    '--use-gl=swiftshader',
    '--use-mock-keychain',
    '--single-process',
    '--headless']

for argument in lambda_options:
    option.add_argument(argument)

driver = webdriver.Chrome(options=option)
driver.set_page_load_timeout(10)
try:
    driver.get(weburl)
    time.sleep(2)
    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, 'lxml')
    meta = soup.find(attrs={"name":"news_keywords"})['content']
    keywords = meta.split(',')
    category = keywords[len(keywords)-1].strip()
    title = soup.findAll("h1",{"class":"header"})[0].string.strip()
    pdate_str = soup.findAll("span",{"class":"entityPublishInfo-meta-info"})[0].string
    
    sql = "UPDATE stories SET story_name_line = %s, line_category = %s , publish_datetime = %s , line_views = %s , line_likes = %s , line_comments = %s  WHERE anvato_id = %s"
    cursor = conn.cursor()
    cursor.execute(sql, (
    title, category, publish_date, views, likes, comments, anvato_id))
    conn.commit()
    cursor.close()
except:
    print('except' + weburl)

conn.close()
driver.close()
import os
os.system("pkill chrome")

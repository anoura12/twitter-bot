from __future__ import unicode_literals
import os
import re
import time
import tweepy
from tweepy import OAuthHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from os import environ

while True:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-sh-usage")
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),options=chrome_options)

    url = "https://covidfightclub.org/"

    browser.get(url)

    get_source = browser.page_source

    soup = BeautifulSoup(get_source, 'html.parser')
    medicine_list = soup.find_all("div", {"class": ["info-tag badge badge-warning", "info-tag badge badge-primary",
                                                    "detail-row city", "detail-row contact-name", "detail-row medicine-name", "detail-row note", "detail-row phone", "detail-row address"]})
    browser.quit()
    j = 0
    l = []
    for i in medicine_list:
        j += 1
        if('detail-row address' in str(i)):
            addr = " ".join(i.text.split())
            l.append(addr)
            continue
        if(j == 5 and ("detail-row note" in str(i))):
            l.append("-")
            note = " ".join(i.text.split())
            l.append(note)
            j = j + 1
            continue
        if(j == 5 and ("detail-row phone" in str(i))):
            l.append("-")
            l.append("-")
            if(a.isnumeric()):
                match_num = re.search(r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$', a)
                if match_num:
                    l.append(a)
                    break
        if(j == 6 and ("detail-row phone" in str(i))):
            l.append("-")
            if(a.isnumeric()):
                match_num = re.search(r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$', a)
                if match_num:
                    l.append(a)
                    break
        a = " ".join(i.text.split())
        if(a.isnumeric()):
                match_num = re.search(r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$', a)
                if match_num:
                    l.append(a)
                    break
        l.append(a)
        if(j % 7 == 0):
            break
  
    CONSUMER_KEY = environ['CONSUMER_KEY']
    CONSUMER_SECRET = environ['CONSUMER_SECRET']
    ACCESS_TOKEN = environ['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']
    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    try:
        badge = l[0]
        city = l[1]
        contactName = l[2]
        requirement = l[3]
        address = l[4]
        info = l[5]
        phone = l[6]

        if len(contactName) == 1:
            raise Exception

        if badge == "Supplier":
            tweet = "This is a {} \nLocation: {} \nName: {} \nSupplying: {} \nAddress: {} \nInfo: {}\nContact No: {}".format(
                    badge.strip(), city.strip(), contactName.capitalize().strip(), requirement.strip(), address.strip(), info.strip(), phone.strip())
            if(len(tweet) > 280):
                tweet = "This is a {} \nLocation: {} \nName: {} \nSupplying: {} \nAddress: {} \nInfo: -\nContact No: {}".format(
                badge.strip(), city.strip(), contactName.capitalize().strip(), requirement.strip(), address.strip(), phone.strip())
            print("Tweet\n"+tweet+"\n")
            api.update_status(status=tweet)
            print("Tweeted")
            time.sleep(30)
        else:
            tweet = "This is a {} \nLocation: {} \nName: {} \nRequirement: {} \nAddress: {} \nInfo: {}\nContact No: {}".format(
                badge, city, contactName.capitalize(), requirement, address, info, phone)
            if(len(tweet) > 280):
                tweet = "This is a {} \nLocation: {} \nName: {} \nRequirement: {} \nAddress: {} \nInfo: -\nContact No: {}".format(
                badge.strip(), city.strip(), contactName.capitalize().strip(), requirement.strip(), address.strip(), phone.strip())
            print("Tweet\n"+tweet+"\n")
            api.update_status(status=tweet)
            print("Tweeted")
            time.sleep(30)
    except:
        print("Error occured")
        time.sleep(60)

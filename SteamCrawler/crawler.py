import socket
import urllib
import urllib.request
import threading
from contextlib import closing
from time import sleep
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import utils

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class GameCrawler:
    def __init__(self,gameType,gamePage):
        self.headers = utils.headers
        self.browser = webdriver.Chrome(r'F:\cdir\chromedriver.exe')
        self.gameType = gameType
        self.gamePage = gamePage

    #Get the page source of steam games
    def getGameInfo(self):
        rows = []
        print("start to crawl" + self.gameType + "and" + str(self.gamePage))
        for sp in range(self.gamePage):
            url = 'https://store.steampowered.com/contenthub/querypaginated/tags/{0}/render/?query=&start={1}&count=15&cc=CN&l=schinese&v=4&tag={2}' \
                .format('TopSellers', sp * 15, urllib.parse.quote(self.gameType))
            response = requests.get(url, utils.headers).text
            com = re.compile('https://store.steampowered.com/app/(.*?)/(.*?)/')
            com1 = re.compile('href="(.*?)"')
            result = re.sub(r'\\', '', response)
            result = re.findall(com1, result)
            print("start to crawl page: %d" % (sp + 1))
            for dat in result:
                game_id = re.findall(com, str(dat))[0][0]
                try:
                    segRes = self.useOfSelenium("https://steamcommunity.com/app/"+str(game_id)+"/reviews/",10)
                    rows.extend(segRes)
                except:
                    pass
            print('page %d finished!' % (sp + 1))
        print(self.gameType + "and" + str(self.gamePage) + "done!")
        print("all work complete!")
        self.browser.close()
        return rows
        
    #Use Selenium to browse the website
    def useOfSelenium(self,url,times):
        self.browser.get(url)
        for _ in range(times):
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(1)
        response = self.browser.page_source
        soup = BeautifulSoup(response,'lxml')
        #extract information from page_source
        segRes = self.getReviewText(soup)
        return segRes
        
    #Extract review Text from page source
    def getReviewText(self,soup):
        comments = soup.findAll(class_=r'apphub_CardTextContent')
        rates = soup.findAll(class_=r'title')
        funnyAndHelpfulList = soup.findAll(class_=r'found_helpful')
        hourPlayedList = soup.findAll(class_=r'hours')
        #Get Comment And List

        commentList = self.getCommentList(comments)
        rateList = self.getRateList(rates)
        helpfulList, funnyList = self.getFunnyAndHelpfulList(funnyAndHelpfulList)
        hourList = self.getHourPlayedList(hourPlayedList)
        title = self.getGameName(soup)

        segRes = []
        for comment,rate,helpful,funny,hour in zip(commentList,rateList,helpfulList,funnyList,hourList):
            combine = (title,comment,rate,helpful,funny,hour)
            segRes.append(combine)
        return segRes
        
    #Get the name of steam games
    def getGameName(self,soup):
        title = soup.findAll(class_=r'apphub_AppName ellipsis')
        title = re.sub('<(.*?)>', '', str(title), 0)
        title = title.replace(r'\t', '').replace(r'\r', '').replace(r'\n', '').strip()
        return title
    
    #Get the helpful and funny review list
    def getFunnyAndHelpfulList(self,funnyAndHelpfulList):
        helpfulList = []
        funnyList = []
        helpfulre = re.compile(r'([0-9]+) [a-z]+? found this review helpful')
        funnyre = re.compile(r'([0-9]+) [a-z]+? found this review funny')
        helpful = 0
        funny = 0
        for fah in funnyAndHelpfulList:
            m = helpfulre.search(str(fah))
            if m:
                helpful = m.group(1)
            n = funnyre.search(str(fah))
            if n:
                funny = n.group(1)
            helpfulList.append(helpful)
            funnyList.append(funny)
        return helpfulList,funnyList
        
    #Get the information of players hour played information
    def getHourPlayedList(self,hourPlayedList):
        hourList = []
        for hour in hourPlayedList:
            hour = re.sub('<(.*?)>', '', str(hour), 0)
            hour = hour.replace(r'\t', '').replace(r'\r', '').replace(r'\n', '').strip()
            hour = float(re.findall('\d+\.\d+',hour)[0])
            hourList.append(str(hour))
        return hourList
    
    #Get Player's comment List
    def getCommentList(self,comments):
        commentList = []
        for comment in comments:
            comment = re.sub('<div class="date_posted">(.*?)</div>','',str(comment),0)
            comment = re.sub('<(.*?)>', '', str(comment), 0)
            comment = comment.replace(r'\t', '').replace(r'\r', '').replace(r'\n', '').strip()
            commentList.append(comment)
        return commentList
    
    #Get Player's recommdation and non-recommdation
    def getRateList(self,rates):
        rateList = []
        for rate in rates:
            rate = re.sub('<(.*?)>', '', str(rate), 0)
            rate = rate.replace(r'\t', '').replace(r'\r', '').replace(r'\n', '').strip()
            if rate == "Not Recommended":
                rateList.append(0)
            else:
                rateList.append(1)
        return rateList




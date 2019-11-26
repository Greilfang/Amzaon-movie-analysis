import time
import random
import threading
import pandas as pd
import numpy as np
import random
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import urllib3
import requests
from requests.cookies import RequestsCookieJar

config={
    'base_url':'https://www.amazon.com/dp/',
    'max_thread_num':1,
    'save_path':'/'
}

def getProductID(path):
    df=pd.read_csv(path)
    return df.values[:,0].tolist()
    
def save_html(target_url,content):
    if content is None:
        return
    file_name=target_url.split('/')[-1]
    print('file_name:',file_name)
    f = open('./moviehtml/'+file_name+'.html','w',encoding='utf-8')
    f.write(content)
    f.close()

def wrapCookie(cookies):
    print('add a new cookie')
    cookie_jar = requests.cookies.RequestsCookieJar()
    resd = requests.utils.dict_from_cookiejar(cookies)
    cookie_jar.set([key for key in resd][0], resd[[key for key in resd][0]], domain='www.amazon.com')
    return cookie_jar


class Crawler:
    def __init__(self,path,config):
        self.IDs = getProductID(path)
        self.config = config
        self.errorIDs=[]
        self.cookie_pool=[]

    def extract_prime_info(self):
        pass
    
    def scheduleCrawling(self):
        #MAX_THREAD_NUM=self.config['max_thread_num']
        BASE_URL=self.config['base_url']
        for i in range(100):
            target_url = BASE_URL + self.IDs[i]
            self.crawl(target_url)
            interval=1+random.random()*3
            time.sleep(interval)
    def requestURL(self,target_url):
        ua=UserAgent()
        response= None
        header = {
        'User-Agent': ua.random,
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6',
        'accept': 'text/html,application/xhtml+xml,application/xml;\
            q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br'
        }
        try:
            if len(self.cookie_pool)==0:
                response = requests.get(target_url,headers=header,timeout=10)
                print('cookie:',response.cookies.items())
                if len(response.cookies.items())!=0:
                    cookie_jar=wrapCookie(response.cookies)
                    self.cookie_pool.append(cookie_jar)
            else:
                cookie_jar=random.sample(self.cookie_pool,1)
                response=requests.get(target_url,headers=header,cookies=cookie_jar,timeout=10)
                if len(response.cookies.items())!=0:
                    cookie_jar=wrapCookie(reponse.cookies)
                    self.cookie_pool.append(cookie_jar)
                    if len(self.cookie_pool>5):self.cookie_pool.pop(0)

        except Exception:
            print('Requests failed')
        if response.status_code == 404:
            print('Resource not found:',target_url)
            return None
        elif response.status_code == 200:
            print('Request successfully:',target_url)
            return response.text
        else:
            print('Status Code:',response.status_code,target_url)
            return response.text

    def crawl(self,target_url):
        content = self.requestURL(target_url)
        if content is None:
            print('target_url:',target_url,'is not found')
        elif content is not None:
            save_html(target_url,content)
            self.extract_prime_info()
        

if __name__ == "__main__":
    crawler = Crawler('productId_0.csv',config)
    crawler.scheduleCrawling()
import time
import calendar
import random
import pandas as pd
import numpy as np
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import urllib3
import requests
from requests.cookies import RequestsCookieJar
from demo import setReview,setMovie
import json
import os,sys,io
import threading
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
demo_target_url = "http://baidu.com"
config={
    'base_url':'https://www.amazon.com/dp/',
    'max_thread_num':1,
    'save_path':'/'
}
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

def getProductID(path):
    df=pd.read_csv(path)
    return df.values[:,0].tolist()
    
def wrapCookie(cookies):
    print('add a new cookie:')
    print(cookies.items())
    cookie_jar = requests.cookies.RequestsCookieJar()
    cookie_jar.update(cookies)
    return cookie_jar

def save_page(content,ID,path='./cnt'):
    print(ID,'saved')
    with open(path+'/'+ID,'w') as file:
        json.dump(content,file)

def save_IDs(ID_list,order,path='./pers/IDs'):
    fpath=path+'_'+str(order)
    with open(fpath,'w') as file:
        json.dump(ID_list,file)

def load_IDs(order,path='./pers/IDs'):
    fpath=path+'_'+str(order)
    with open(fpath,'r') as file:
        ID_list=json.load(file)
    return ID_list


class Crawler:
    def __init__(self,path,config):
        self.IDs = getProductID(path)
        self.config = config
        self.errorIDs=[]
        self.cookie_pool=[]
        self.cookie_jar=requests.cookies.RequestsCookieJar()
        self.misses=0

    def extract(self,content,ID):
        soup=BeautifulSoup(content,'lxml')
        movie=setMovie()
        movie['ID']=ID
        title_alpha = soup.find('title').string.split(' ')[0]
        if title_alpha == 'Watch':
            title=soup.find('h1')
            movie['Title']=title.string if title else None
            intro=soup.find('p',{'class':'_1npiSz'})
            movie['Intro']=intro.string if intro else None
            imdb=soup.find('span',{'data-automation-id': 'imdb-rating-badge'})
            movie['IMDB']=float(imdb.string) if imdb else None
            score=soup.find('span',{'class':'a-icon-alt'})
            movie['Score']=float(score.string.split()[0]) if score else None 
            yr=soup.find('span',{'data-automation-id':'release-year-badge'})
            movie['Year']=int(yr.string) if yr else None
            
            prime_html=soup.find_all('div',{'class':'_1ONDJH'})[0].find_all('dl')
            
            try:
                genre_html=prime_html[0]
                if genre_html.dt.span.string=='Genres':
                    genres=genre_html.find_all('a')
                    for genre in genres:
                        movie['Genre'].append(genre.string)
            except Exception:
                print('Genre exception')
            
            try:
                director_html=prime_html[1]
                if director_html.dt.span.string=='Director':
                    directors=director_html.find_all('a')
                    for director in directors:
                        movie['Director'].append(director.string)
            except Exception:
                print('Director Exception')
            try:
                starring_html=prime_html[2]
                if starring_html.dt.span.string=='Starring':
                    starrings=starring_html.find_all('a')
                    for starring in starrings:
                        movie['Starring'].append(starring.string)
            except Exception:
                print('Starring exception')
            try:
                more_html=soup.find_all('div',{'class':'_1ONDJH'})[1].find_all('dl')
                if more_html:
                    supporting_html=more_html[0]
                    if supporting_html.dt.span.string=='Supporting actors':
                        supportings=supporting_html.find_all('a')
                        for supporting in supportings:
                            movie['Supporting'].append(supporting.string)
            except Exception:
                print('Support exception')

            reviews=soup.find('div',{'id':'cm-cr-dp-review-list'}).find_all('div',{'class':'a-section review aok-relative'})
            if reviews:
                for rv in reviews:
                    try:
                        review=setReview()
                        review['Profile']=rv.find('span',{'class':'a-profile-name'}).string
                        review['Score']=float(rv.find('i',{'data-hook':'review-star-rating'}).span.string.split(' ')[0])
                        month,year,day=rv.find('span',{'data-hook':'review-date'}).string.split(' ')
                        review['Moment']['Year']=int(year)
                        review['Moment']['Month']=list(calendar.month_name).index(month)
                        review['Moment']['Day']=int(day)
                        review['Summary']=rv.find('a',{'data-hook':'review-title'}).span.string
                        review['Text']=rv.find('div',{'data-hook':'review-collapsed'}).span.string
                        helpful=rv.find('span',{'data-hook':'helpful-vote-statement'}).string
                        if helpful is not None:
                            helpful=helpful.split(' ')[0]
                            review['Helpful'] = 1 if helpful=='One' else int(helpful)
                    except Exception:
                        pass
                        #print('complex review exception')
                    movie['Reviews'].append(review)
            return movie
        elif title_alpha == 'Amazon.com:':
            title=soup.find('span',{'id':'productTitle'})
            movie['Title']=title.string.replace('\n','').strip(' ') if title else None
            movie['IMDB'] = None
            movie['Supporting']=None
            product_lis = soup.find('td',{'class':'bucket'}).find_all('li')
            if product_lis:
                for pli in product_lis:
                    #print('pli:',pli.b)
                    plib = pli.b
                    if plib is None:
                        continue
                    elif plib.string == 'Actors:':
                        actors=pli.find_all('a')
                        for actor in actors:
                            movie['Starring'].append(actor.string)
                    elif plib.string =='Directors:':
                        directors=pli.find_all('a')
                        for director in directors:
                            movie['Director'].append(director.string)
                    elif plib.string=='VHS Release Date:':
                        movie['Year']=int(pli.b.next_sibling.string.split(' ')[-1])

            score=soup.find('span',{'data-hook':'rating-out-of-text'})
            movie['Score']=float(score.string.split(' ')[0]) if score else None
            
            reviews=soup.find('div',{'class':'card-padding'}).find_all('div',{'class':'a-section celwidget'})
            if reviews:
                for rv in reviews:
                    try:
                        review=setReview()
                        review['Profile']=rv.find('span',{'class':'a-profile-name'}).string
                        month_day,year=rv.find('span',{'data-hook':'review-date'}).string.split(',')
                        review['Moment']['Year']=int(year)
                        review['Moment']['Month']=list(calendar.month_name).index(month_day.split(' ')[0])
                        review['Moment']['Day']=int(month_day.split(' ')[1])
                        review['Score']=float(rv.find('i',{'data-hook':'review-star-rating'}).span.string.split(' ')[0])
                        movie['Reviews'].append(review)
                        review['Summary']=rv.find('a',{'data-hook':'review-title'}).span.string
                        review['Text']=rv.find('div',{'data-hook':'review-collapsed'}).span.string
                        helpful=rv.find('span',{'data-hook':'helpful-vote-statement'}).string
                        if helpful is not None:
                            helpful=helpful.split(' ')[0]
                            review['Helpful'] = 1 if helpful=='One' else int(helpful)
                    except Exception:
                        pass
                        #print('simple review exception!!!')
            return movie
        elif title_alpha == 'Robot':
            print('Robot Check:',ID)
            return None
        return None
    
    def scheduleCrawling(self,order):
        BASE_URL=self.config['base_url']
        success_count=0
        if os.path.isfile('./pers/IDs_{}'.format(order)):
            self.IDs=load_IDs(order)
            print(order,'ok')
        
        retry_count = 5
        pools_requests = requests.get('http://http.tiqu.alicdns.com/getip3?num=5&type=2&pro=&city=0&yys=100017&port=11&pack=77240&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=').json()
        proxy_pool=pools_requests['data']
        print(proxy_pool)
        proxy = proxy_pool.pop()
        del proxy['outip']
        print('new_proxy:',proxy)
        while len(self.IDs)!=0:
            ID = self.IDs.pop(0)
            target_url = BASE_URL + ID
            extracted_content = self.crawl(target_url,proxy)
            if extracted_content is not None:
                save_page(extracted_content,ID)
                success_count=success_count+1
            else:
                self.IDs.append(ID)
                retry_count=retry_count-1
                if retry_count ==0:
                    while len(proxy_pool)==0:
                        pools_requests = requests.get('http://http.tiqu.alicdns.com/getip3?num=5&type=2&pro=&city=0&yys=100017&port=11&pack=77240&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=').json()
                        time.sleep(1+random.random())
                        proxy_pool=pools_requests['data']
                    proxy=proxy_pool.pop()
                    del proxy['outip']
                    print('new_proxy:',proxy)
                    #delete_proxy(proxy)
                    retry_count=5
                    #proxy=get_proxy().get("proxy")
            if success_count%20==0 and success_count!=0:
                save_IDs(self.IDs,order)
                print('----------ID renewed!---------')
                time.sleep(2+2*random.random())
            print('---------------------------------------')
            
            
            interval=3+random.random()*2.8
            time.sleep(interval)




    def requestURL(self,target_url,proxy):
        ua=UserAgent()
        response= None
        header = {
        'User-Agent': ua.random,
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6',
        'accept': 'text/html,application/xhtml+xml,application/xml;\
            q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br'
        }
        proxyMeta = "https://%(host)s:%(port)s" % {
            "host" : proxy['ip'],
            "port" : proxy['port']
            }
        proxies = {
            "https":proxyMeta
            }
        if len(self.cookie_pool)==0:
            try:
                #response = requests.get(target_url,headers=header,proxies={"http": "http://{}".format(proxy)},timeout=4)
                response = requests.get(target_url,headers=header,proxies=proxies,timeout=4)
                #print('-----------check proxy----------')
                #print(response.text)
            except:
                return None
            if len(response.cookies.items())!=0:
                print('cookie:',response.cookies.items())
                cookie_jar=wrapCookie(response.cookies)
                self.cookie_pool.append(cookie_jar)
                print('present cookie pool length:',len(self.cookie_pool))
        else:
            prop=random.random()
            cookie_jar=random.sample(self.cookie_pool,1)[0]
            try:
                if prop<0.15:
                    #response=requests.get(target_url,headers=header,proxies={"http": "http://{}".format(proxy)},timeout=4)
                    response=requests.get(target_url,headers=header,proxies=proxies,timeout=4)
                else:
                    #response=requests.get(target_url,headers=header,proxies={"http": "http://{}".format(proxy)},cookies=cookie_jar,timeout=4)
                    response=requests.get(target_url,headers=header,proxies=proxies,cookies=cookie_jar,timeout=4)
            except:
                return None
            if len(response.cookies.items())!=0:
                cookie_jar=wrapCookie(response.cookies)
                self.cookie_pool.append(cookie_jar)
                if len(self.cookie_pool)>15:
                    self.cookie_pool.pop(0)
                print('present cookie pool length:',len(self.cookie_pool))

        if response.status_code == 404:
            print('Resource not found:',target_url)
            return None
        else:
            return response.text
        return None

    def crawl(self,target_url,proxy):
        content = self.requestURL(target_url,proxy)
        extracted_content=None 
        if content is None:
            print('target_url:',target_url,'is not found')
        elif content is not None:
            ID=target_url.split('/')[-1]
            print('current ID:',ID)
            try:
                extracted_content= self.extract(content,ID)
            except:
                self.misses=self.misses+1
                print('self.misses:',self.misses)

        return extracted_content
        

if __name__ == "__main__":
    #sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    #sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    #crawler = Crawler('productId_0.csv',config)
    spider_list=[]
    for i in range(8):
        crawler = Crawler('productId_0.csv',config)
        threading.Thread(target=crawler.scheduleCrawling,args=(i,)).start()
        print('Spider {} start'.format(i))
        time.sleep(3)

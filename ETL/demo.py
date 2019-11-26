import time
import calendar
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
import lxml
import re


def setMovie():
    movie={
        'ID':None,
        'Title':None,
        'Intro':None,
        'IMDB':-1,
        'Score':-1,
        'Year':-1,
        'MPAA':None,
        'Genre':[],
        'Director':[],
        'Starring':[],
        'Supporting':[],
        'Reviews':[]
    }
    return movie
def setReview():
    review={
        'Profile':None,
        'Moment':{'Year':-1,'Month':-1,'Day':-1},
        'Score':-1,
        'Summary':None,
        'Text':None,
        'Helpful':0
    }
    return review
def extract(ID='1929951019'):
    soup=BeautifulSoup(open('./moviehtml/1929951019.html',encoding='utf-8'),'lxml')
    movie=setMovie()
    movie['ID']=ID
    title_alpha = soup.find('title').string.split(' ')[0]
    if title_alpha == 'Watch':
        movie['Title']=soup.find('h1').string
        movie['Intro']=soup.find('p',{'class':'_1npiSz'}).string
        movie['IMDB']=float(soup.find('span',{'data-automation-id': 'imdb-rating-badge'}).string)
        movie['Score']=float(soup.find('span',{'class':'a-icon-alt'}).string.split()[0])
        movie['Year']=int(soup.find('span',{'data-automation-id':'release-year-badge'}).string)
        print(movie.items())
        #y=soup.find_all('dl')[0]
        
        prime_html=soup.find_all('div',{'class':'_1ONDJH'})[0].find_all('dl')
        
        genre_html=prime_html[0]
        if genre_html.dt.span.string=='Genres':
            genres=genre_html.find_all('a')
            for genre in genres:
                movie['Genre'].append(genre.string)
        director_html=prime_html[1]
        if director_html.dt.span.string=='Director':
            directors=director_html.find_all('a')
            for director in directors:
                movie['Director'].append(director.string)
        starring_html=prime_html[2]
        if starring_html.dt.span.string=='Starring':
            starrings=starring_html.find_all('a')
            for starring in starrings:
                movie['Starring'].append(starring.string)
        
        more_html=soup.find_all('div',{'class':'_1ONDJH'})[1].find_all('dl')
        supporting_html=more_html[0]
        if supporting_html.dt.span.string=='Supporting actors':
            supportings=supporting_html.find_all('a')
            for supporting in supportings:
                movie['Supporting'].append(supporting.string)
        
        review_html=soup.find('div',{'id':'cm-cr-dp-review-list'})
        reviews=review_html.find_all('div',{'class':'a-section review aok-relative'})
        for rv in reviews:
            review=setReview()
            review['Profile']=rv.find('span',{'class':'a-profile-name'}).string
            review['Score']=float(rv.find('i',{'data-hook':'review-star-rating'}).span.string.split(' ')[0])
            month,year,day=rv.find('span',{'data-hook':'review-date'}).string.split(' ')
            review['Moment']['Year']=year
            review['Moment']['Month']=month
            review['Moment']['Day']=day
            review['Summary']=rv.find('a',{'data-hook':'review-title'}).span.string
            review['Text']=rv.find('div',{'data-hook':'review-collapsed'}).span.string
            helpful=rv.find('span',{'data-hook:helpful-vote-statement'})
            if helpful is not None:
                helpful=helpful.split(' ')[0]
                review['Helpful'] = 1 if helpful=='One' else int(helpful) 
            movie['Reviews'].append(review)
    elif title_alpha == 'Amazon.com:':
        movie['Title']=soup.find('span',{'id':'productTitle'}).string.replace('\n','').strip(' ')
        movie['IMDB'] = None
        movie['Supporting']=None
        product_lis = soup.find('td',{'class':'bucket'}).find_all('li')
        for pli in product_lis:
            if pli.b.string == 'Actors:':
                actors=pli.find_all('a')
                for actor in actors:
                    movie['Starring'].append(actor.string)
            elif pli.b.string =='Directors:':
                directors=pli.find_all('a')
                for director in directors:
                    movie['Director'].append(director.string)
            elif pli.b.string=='VHS Release Date:':
                movie['Year']=int(pli.b.next_sibling.string.split(' ')[-1])

        movie['Score']=float(soup.find('span',{'data-hook':'rating-out-of-text'}).string.split(' ')[0])

    print(movie)


if __name__ == "__main__":
    extract()
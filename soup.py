#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import re
import os
import sys
import nltk
nltk.download('punkt')
nltk.download('stopwords')

from elasticsearch import Elasticsearch
from konlpy.tag import Okt
from collections import Counter
from nltk.corpus import stopwords
 
def data_text_cleaning(data):
 
    # 영문자 이외 제거
    only_english = re.sub('[^a-zA-Z]', ' ', data)
 
    # 소문자 변환
    no_capitals = only_english.lower().split()
 
    # 불용어 제거
    stops = set(stopwords.words('english'))
    stemmer_words = [word for word in no_capitals if not word in stops]
 
    return stemmer_words


def kfilter(s):
    return re.sub(u'[^ \.\,\?\!\u3130-\u318f\uac00-\ud7a3]+','',s)


es_host="127.0.0.1"
es_port="9200"

if __name__ == '__main__':
    try:
        ##########################################################
        ##USA
    
        URL = 'https://www.youtube.com/feed/explore/?gl=GB'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="utf8")
        search_results = soup.findAll("script")

        # script section of the soup
        y = str(search_results)

        my_para = []

        # first iteration of the title
        pos = y.find("""title":{"runs":[{"text":""")
        pos_x = pos + 25
        k = y[pos_x:pos+200]
        pos_r = y[pos_x:pos+200]
        sub = """}]"""
        pos_end = pos_x + k.find(sub) - 1

        my_para.append(y[pos_x:pos_end])
         #print(y[pos_x:pos_end])

        # repetition
        i = 1

        while i <= 50:
            pos = y.find("""title":{"runs":[{"text":""", pos_x)
            pos_x = pos + 25
            k = y[pos_x:pos+200]
            pos_r = y[pos_x:pos+200]
            sub = """}]"""
            pos_end = pos_x + k.find(sub) - 1

            my_para.append(y[pos_x:pos_end])
            
           
            i += 1

        okt = Okt()
        word_d = {}
        words = []
        weight = 60
        
        for para in my_para:
    
             noun = data_text_cleaning(para)
             for n in noun:
                cnt = 0
                  #offical video, 광고, short태그 등은 유의미하지않으므로 제거
                if(n=='official'or n== 'video' or n== 'ad' or n== 'short' or n=='shorts' or n== 'vs') :
                    continue
                if(len(n)>1):
                    while cnt < weight//10:
                      words.append(n)
                      cnt = cnt +1
            
        weight = weight-1
        
        count = Counter(words)

        noun_list = count.most_common(10)
        for v in noun_list:
                print(v)

        print("---------------------------------------------")
        #가중치 계산한 값을 각각 리스트에 저장

        chart_words = []
        chart_freq = []

        for n in noun_list:
            chart_words.append(n[0])
            chart_freq.append(n[1])
        
        print(chart_words)
        print("---------------------------------------------")
        print(chart_freq)

        print("---------------------------------------------")
        # elasticsearch에 저장

        es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
        e={'url':URL,'words':chart_words,'frequencies':chart_freq}

        docs = es.search(index = 'usa')
        id = docs['hits']['total']['value']

        source = es.index(index='usa', doc_type='chart', id = id+1, body = e)
        print(source)

        ##########################################################
        ##CA
        URL = 'https://www.youtube.com/feed/explore/?gl=CA'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="utf8")
        search_results = soup.findAll("script")

        # script section of the soup
        y = str(search_results)

        my_para = []

        # first iteration of the title
        pos = y.find("""title":{"runs":[{"text":""")
        pos_x = pos + 25
        k = y[pos_x:pos+200]
        pos_r = y[pos_x:pos+200]
        sub = """}]"""
        pos_end = pos_x + k.find(sub) - 1

        my_para.append(y[pos_x:pos_end])
         #print(y[pos_x:pos_end])

        # repetition
        i = 1

        while i <= 50:
            pos = y.find("""title":{"runs":[{"text":""", pos_x)
            pos_x = pos + 25
            k = y[pos_x:pos+200]
            pos_r = y[pos_x:pos+200]
            sub = """}]"""
            pos_end = pos_x + k.find(sub) - 1

            my_para.append(y[pos_x:pos_end])
            
           
            i += 1

        okt = Okt()
        word_d = {}
        words = []
        weight = 60
        
        for para in my_para:
    
             noun = data_text_cleaning(para)
             for n in noun:
                cnt = 0
                  #offical video, 광고, short태그 등은 유의미하지않으므로 제거
                if(n=='official'or n== 'video' or n== 'ad' or n== 'short' or n=='shorts' or n== 'vs') :
                    continue
                if(len(n)>1):
                    while cnt < weight//10:
                      words.append(n)
                      cnt = cnt +1
            
        weight = weight-1
        
        count = Counter(words)

        noun_list = count.most_common(10)
        for v in noun_list:
            print(v)
        
        print("---------------------------------------------")
        #가중치 계산한 값을 각각 리스트에 저장

        chart_words = []
        chart_freq = []

        for n in noun_list:
            chart_words.append(n[0])
            chart_freq.append(n[1])
        
        print(chart_words)
        print("---------------------------------------------")
        print(chart_freq)

        print("---------------------------------------------")
        # elasticsearch에 저장

        es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
        e={'url':URL,'words':chart_words,'frequencies':chart_freq}

        docs = es.search(index = 'canada')
        id = docs['hits']['total']['value']

        source = es.index(index='canada', doc_type='chart', id = id+1, body = e)
        print(source)

        ##########################################################
        ##KR
        URL = 'https://www.youtube.com/feed/explore/?gl=KR'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="utf8")
        search_results = soup.findAll("script")

        # script section of the soup
        y = str(search_results)

        my_para = []

        # first iteration of the title
        pos = y.find("""title":{"runs":[{"text":""")
        pos_x = pos + 25
        k = y[pos_x:pos+200]
        pos_r = y[pos_x:pos+200]
        sub = """}]"""
        pos_end = pos_x + k.find(sub) - 1

        my_para.append(y[pos_x:pos_end])
         #print(y[pos_x:pos_end])

        # repetition
        i = 1

        while i <= 50:
            pos = y.find("""title":{"runs":[{"text":""", pos_x)
            pos_x = pos + 25
            k = y[pos_x:pos+200]
            pos_r = y[pos_x:pos+200]
            sub = """}]"""
            pos_end = pos_x + k.find(sub) - 1

            my_para.append(y[pos_x:pos_end])
            
           
            i += 1

        okt = Okt()
        word_d = {}
        words = []
        weight = 60
        
        for para in my_para:
            hsent = kfilter(para)
            noun = okt.nouns(hsent)
            for n in noun:
                cnt = 0
                if(n=='방송'):
                    continue
                if(len(n)>1):
                    while cnt < weight//10:
                        words.append(n)
                        cnt = cnt +1
            
        weight = weight-1
        
        count = Counter(words)

        noun_list = count.most_common(10)
        for v in noun_list:
          print(v)
        
        print("---------------------------------------------")
        #가중치 계산한 값을 각각 리스트에 저장

        chart_words = []
        chart_freq = []

        for n in noun_list:
            chart_words.append(n[0])
            chart_freq.append(n[1])
        
        print(chart_words)
        print("---------------------------------------------")
        print(chart_freq)

        print("---------------------------------------------")
        # elasticsearch에 저장
        es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
        e={'url':URL,'words':chart_words,'frequencies':chart_freq}

        docs = es.search(index = 'korea')
        id = docs['hits']['total']['value']

        source = es.index(index='korea', doc_type='chart', id = id+1, body = e)
        print(source)



    except BaseException:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())

    """ 
    finally:
        print("\n" + "Press 'Enter' to close the window :)")
        input() 
    """

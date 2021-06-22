#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import re
import os
import sys
from elasticsearch import Elasticsearch
from konlpy.tag import Okt
from collections import Counter
 
def hfilter(s):
    return re.sub(u'[^ \u3130-\u318f\uac00-\ud7a3]+','',s)

es_host="127.0.0.1"
es_port="9200"

if __name__ == '__main__':
    try:
        URL = 'https://www.youtube.co.kr/feed/explore'
     
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

        print("---------------------------------------------")
        # 제목리스트 출력
        print(my_para)

        print("---------------------------------------------")
        # 제목에서 단어를 추출해 가중치 계산
        
        okt = Okt()
        word_d = {}
        words = []
        weight = 60

        for para in my_para:
            hsent = hfilter(para)
            print(hsent)

            noun = okt.nouns(hsent)
            print(noun)

            for n in noun:
                cnt = 0
                if(len(n)>1):
                    while cnt < weight//10:
                        words.append(n)
                        cnt = cnt +1
            
            weight = weight-1
        
        count = Counter(words)

        noun_list = count.most_common(100)
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
        e={'url':URL, 'words':chart_words, 'frequencies':chart_freq}

        source = es.index(index='Chart', doc_type='chart', id = 1, body = e)
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

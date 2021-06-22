#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import re
import os
from konlpy.tag import Okt
from collections import Counter
import cosine
 
def hfilter(s):
    return re.sub(u'[^ \u3130-\u318f\uac00-\ud7a3]+','',s)

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

        #print("---------------------------------------------")
        #print(my_para)
        #print("---------------------------------------------")
       
        
        okt = Okt()
        word_d = {}
        words = []
        weight = 60

        for para in my_para:
            hsent = hfilter(para)
            #print(hsent)

            noun = okt.nouns(hsent)
            #print(noun)

            for n in noun:
                cnt = 0
                if(len(n)>1):
                    while cnt < weight//10:
                        words.append(n)
                        cnt = cnt +1
            
            weight = weight-1
        
        count = Counter(words)

        noun_list = count.most_common(100)
        ("---------------------------------------------")
        
        f = open("input.txt", 'a+')

        for v in noun_list:
          print(v)
          f.write(v[0])
        f.write("\n")
        f.close()

        f = open("input.txt", 'r')
        line = f.readline() 
        line = line.strip() #줄 바꿈 (\n) 제거
        recent = line
        print(recent) #1번째 줄입니다.

        line = f.readline()
        line = line.strip() 
        past = line
        print(past) #2번째 줄입니다.

        f.close()

        cosine.cosine(recent, past)


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
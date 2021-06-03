from bs4 import BeautifulSoup
import requests
import re
import os


if __name__ == '__main__':
    try:
        URL = 'https://www.youtube.co.kr/feed/explore'


        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="utf8")
        search_results = soup.findAll("script")

        # script section of the soup
        y = str(search_results)

        # first iteration of the title
        pos = y.find("""title":{"runs":[{"text":""")
        pos_x = pos + 25
        k = y[pos_x:pos+200]
        pos_r = y[pos_x:pos+200]
        sub = """}]"""
        pos_end = pos_x + k.find(sub) - 1
        #print(y[pos_x:pos_end])

        # repetition
        i = 1
        f = 55

        while i <= f:
            pos = y.find("""title":{"runs":[{"text":""", pos_x)
            pos_x = pos + 25
            k = y[pos_x:pos+200]
            pos_r = y[pos_x:pos+200]
            sub = """}]"""
            pos_end = pos_x + k.find(sub) - 1
            if i>=6 : print(y[pos_x:pos_end])

            i += 1

    except BaseException:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
    finally:
        print("\n" + "Press 'Enter' to close the window :)")
        input()
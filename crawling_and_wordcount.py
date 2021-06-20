from bs4 import BeautifulSoup
import requests
import re
import os


if __name__ == '__main__':
    try:
        URL = 'https://www.youtube.com/feed/explore'
        f = open("data.txt", 'w')

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

        while i <= 50:
            pos = y.find("""title":{"runs":[{"text":""", pos_x)
            pos_x = pos + 25
            k = y[pos_x:pos+200]
            pos_r = y[pos_x:pos+200]
            sub = """}]"""
            pos_end = pos_x + k.find(sub) - 1
            f.write(y[pos_x:pos_end])
            i += 1
        f.close()

        file = open("data.txt", 'r')
        delete = re.sub("""!@#$%^&*()_-+={[}]|\;:"‘'·<>?/., """, "", file.read())
        read = delete.split()
        relen = len(read)
        print("단어 수: %d" % relen)
        Di = {}
        for i in range(relen):
            plus = 0
            for j in range(relen):
                if read[i] == read[j]:
           	          plus += 1
            Di[read[i]] = plus
        As = sorted(Di.items(), key=lambda x: x[1], reverse=True)

        Dil = len(Di)

        for g in range(Dil):
	        print("\'%s\'의 개수 : %s" % (As[g][0], As[g][1]))

        
        f.close()



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
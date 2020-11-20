import urllib.request
import urllib.parse
import re
import jieba
import chardet
from html.parser import HTMLParser
import time


pagelist = []
newslist = []
jiebalist = []
index = dict()
cnt = 0



class MyHtmlParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag=='a':
            for name,value in attrs:
                if name == 'href':
                    if pagelist.count(value) == 0:
                        pagelist.append(value)
                    match = re.match("http://[a-z]*?\.people\.com\.cn/n\d/2018/\d\d\d\d/[a-z0-9]*?-[0-9]*?\.html",value)
                    if (match!= None):
                        if (value[7] == 't' and value[8] == 'v'):
                            return
                        elif (value[7] == 'p' and value[8] == 'i' and value[9] == 'c'):
                            return
                        try:
                            resp = urllib.request.urlopen(value)
                            html = resp.read().decode("GBK")
                        except:
                            return
                        if newslist.count(value) > 0:#保证不重复
                            return
                        newslist.append(value)
                        global cnt
                        filename = str(cnt)
                        file = open(filename,'w')
                        file.write(html)
                        file.close()
                        #print("cnt ",cnt)
                        cnt = cnt + 1








resp = urllib.request.urlopen("http://www.people.com.cn/")
html = resp.read().decode("GBK")
parser = MyHtmlParser()
parser.feed(html)
point = 0
while pagelist.__len__() < 100000000 :
    try:
        url = pagelist[point]
        #print(url)
        #print("point",point)
        #print (pagelist.__len__())
        resp = urllib.request.urlopen(url)
        html = resp.read()
        html = html.decode("GBK")
        parser.feed(html)
        point = point + 1
        #print("cnt:", cnt)
        time.sleep(0.5)
    except:
        point = point + 1
        continue

print(pagelist.__len__())
print("end. cnt:",cnt)




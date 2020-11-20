from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
import jieba
import pickle
import math
import time
cnt = 4136


file = open("data/newspkg",'rb+')

news = pickle.load(file)
file.close()
#print(news[18])
file2 = open('data/indexpkg','rb+')
index = pickle.load(file2)
file2.close()
#print(index["习近平"])

 #二重字典
file3 = open('data/rcmd','rb+')
rcmd = pickle.load(file3)
file3.close()
#print(rcmd)

#制作新闻缩略图
newspiece = dict()
for key,value in news.items():
    value0 = value[0]
    if (value0.__len__() > 20):
        value0 = value0[0:20] + "..."
    value1 = value[1]
    value2 = value[2]
    if (value2.__len__() > 200):
        value2 = value2[0:200] + "..."
    newspiece[key] = [value0,value1,value2]
#print(newspiece[0])



#查找关键词
def searchfor(keyword,timefilter,date1,date2):
    resultdict = {}
    deltatime = 0
    keywordlist = keyword.split(" ")
    time1 = time.time()
    for key in keywordlist:
        if key in index:
            list = index[key]
            for ind in list:#所有含有此词的新闻ID
                if (timefilter==True) and (newspiece[ind][1] < date1 or newspiece[ind][1] > date2):
                    continue
                if ind in resultdict.keys():
                    resultdict[ind][3] = resultdict[ind][3] + 1
                else:
                    cont = news[ind][2]
                    pos = cont.find(key)
                    if pos>0:
                        cont = "..."+cont[pos:]
                    if len(cont) > 200:
                        cont = cont[0:200] + "..."
                    resultdict[ind] = [newspiece[ind][0], newspiece[ind][1], cont,1]
    deltatime = round((time.time() - time1) * 1000, 2)
    resultdict = sorted(resultdict.items(),key = lambda x:x[1][3],reverse=True)
    #deltatime = round((time.time() - time1)*1000,2)
    return resultdict,deltatime

#主页重定向
def homeroot(request):
    return HttpResponseRedirect("/1")

#主页分页码
def home(request,pages = "1"):
    pagesint = int(pages)
    newspiece_ = dict()
    pagetotal = math.ceil(cnt/30)
    pagelist = range(1,pagetotal + 1)
    for i in range((pagesint-1)*30,pagesint*30):
        if (i > cnt - 1):
            break
        newspiece_[i] = newspiece[i]
    return render_to_response("homepage.html",{"newstotal":cnt,"newsdisplay":newspiece_,"pagenow":pagesint,"pagelist":pagelist});

#搜索页
def engine(request):
    month = range(1,13)
    day = range(1,32)
    return render_to_response("search.html",{"monthlist":month,"daylist":day})


#结果页
@csrf_protect
@csrf_exempt
def result(request,pages = "1"):
    key = request.POST['keyword']
    if (key == ""):
        return HttpResponseRedirect("/search")
    y1 = request.POST['y1']
    m1 = request.POST['m1']
    d1 = request.POST['d1']
    y2 = request.POST['y2']
    m2 = request.POST['m2']
    d2 = request.POST['d2']
    timefilter = True
    if (y1 == "0" or m1 =="0" or d1=="0" or y2 == "0" or m2 =="0" or d2=="0"):
        timefilter = False
    date1 = y1+'-'+m1+'-'+d1
    date2 = y2+'-'+m2+'-'+d2
    print(date1)
    print(date2)
    resultdict,time = searchfor(key,timefilter,date1,date2)
    resulttotal = resultdict.__len__()
    pagesint = int(pages)
    pagetotal = math.ceil(resultdict.__len__()/10)
    pagelist = range(1,pagetotal + 1)
    resultdict_ = []
    for i in range((pagesint-1)*10,pagesint*10):
        if (i >= resultdict.__len__()):
            break
        resultdict_.append(resultdict[i])
    return render_to_response("result.html",{"total":resulttotal,"y1":y1,"m1":m1,"d1":d1,"y2":y2,"m2":m2,"d2":d2,"timefilter":timefilter,\
        "time": time,"keyword": key, "resultdict":resultdict_, "pagelist":pagelist, "pagenow":pagesint})


def admin(request):
    return HttpResponse("admin~~")

#新闻页
def page(request,ind):
    ind = int(ind)
    recmd = {}
    if ind in rcmd.keys():
        recmd = rcmd[ind]
    print(type(rcmd[ind]))
    print(type(recmd))
    return render_to_response("news.html",{"news_con":news[ind],"recmd": recmd})


#python manage.py runserver
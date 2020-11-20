import pickle
import jieba
from jieba import analyse
tfidf = analyse.extract_tags

file = open('newspkg','rb+')
news = pickle.load(file)
#print(news)
rcmd = {}
fenci = {}

for key,value in news.items():
    print(key)
    list1 = list(tfidf(value[0]))
    list2 = list(tfidf(value[2]))
    list1.extend(list2)
    fenci[key] = list1

#rcmd={0:{222:"xxx",223:"xxx",333:"xxx"},1:{...},...}
print("fenci done.")

for key in fenci.keys():
    print("simi",key)
    simlist = []
    for key2 in fenci.keys():
        if key != key2:
            jiao = [val for val in fenci[key] if val in fenci[key2]]
            simila = len(jiao)
            simlist.append([key2,simila])
    simlist = sorted(simlist,key=lambda x:x[1],reverse=True)
    rcmd[key] = {}
    for i in range(0,10):
        if len(rcmd[key]) > 3:
            break
        if news[simlist[i][0]][0] in rcmd[key].values():
            continue
        elif news[simlist[i][0]][0] == news[key][0]:
            continue
        #print(simlist[i][0],news[simlist[i][0]][0])
        rcmd[key][simlist[i][0]] = news[simlist[i][0]][0]



print(rcmd)

file = open('rcmd','wb+')

pickle.dump(rcmd,file,0)

file.close()

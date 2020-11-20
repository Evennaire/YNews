import re
import jieba
import pickle
from html.parser import HTMLParser
cnt = 4136

index = dict() #分词倒排索引
news = dict() #新闻索引

class MyNewsParser(HTMLParser):
    istitle = False
    isdata = False
    title = ""
    date = ""
    text = ""
    def handle_starttag(self, tag, attrs):
        if tag == "h1":
            self.istitle = True
        if tag == "meta":
            if attrs[0][1] =="publishdate":
                self.date = attrs[1][1]
        if tag == "p":
            for name,value in attrs:
                if (name=="class" and value =="img"):
                    return
            self.isdata = True
    def handle_data(self, data):
        if self.istitle == True:
            self.title = data
            self.istitle = False
        if self.isdata == True:
            if (data == "") :
                self.isdata = False
                return
            if (data.find("登录人民网通行证")>-1 or data.find("记住登录状态")>-1 or data.find("忘记密码？")>-1
                or data.find("推荐帖子")>-1 or data.find("发表成功")>-1 or data.find("自动返回")>-1
                    or data.find("请牢记你的用户名")>-1 or data.find("留言板")>-1 or data.find("人民网")>-1
                    or data.find("互联网新闻信息服务许可证")>-1 or data.find("信息网络传播视听节目许可证")>-1
                    or data.find("网络文化经营许可证")>-1 or data.find("网络文化经营许可证")>-1
                    or data.find("人民日报社概况") > -1 or data.find("微信“扫一扫”添加“学习微平台”")>-1
                    or data.find("京网文") > -1 or data.find("人 民 网") > -1
                    or data.find("如何10秒种一棵树") > -1 or data.find("首尔旅行攻略") > -1
                    or data.find("廉政唱出来") > -1 or data.find("猿猴赖上警察妈妈") > -1
                    or data.find("湖北黄陂美味豆丝") > -1 or data.find("武汉百步亭万家宴") > -1
                    or data.find("镜像:") > -1 or data.find("石峁遗址现金字塔式建筑") > -1
                    or data.find("朝鲜啦啦队抵韩") > -1 or data.find("年终奖PK大赛来袭") > -1):
                self.isdata = False
                return
            self.text = self.text + "\n\t" + data + "\r\n"
            self.isdata = False


parser = MyNewsParser()
for i in range(0,cnt):
        print(i)
        #提取title，date，text
        file = open(str(i),'r')
        html = file.read()
        parser.text = ""
        parser.title = ""
        parser.date = ""
        parser.feed(html)
        #if i == 0:
            #print(parser.title)
           # print(parser.date)
            #print(parser.text)
        parser.text = re.sub(r'\s{5,}',"\n",parser.text)
        parser.title = " ".join(parser.title.split("\xa0"))



        #索引
        news[i] = [parser.title,parser.date,parser.text]


        #记录
        file = open(str(i)+".txt",'w+',encoding="UTF-8")
        file.write("Title: " + parser.title+"\n")
        file.flush()
        file.write("Date: "+ parser.date+ "\n")
        file.flush()
        file.write("Text:\n" + parser.text)
        file.flush()
        file.close()

        #分词
        list1 = list(jieba.cut_for_search(parser.title))
        list2 = list(jieba.cut_for_search(parser.text))
        list1.extend(list2)
        for word in list1:
            if (word == "，" or word =='。' or word =='！' or word == '？' or word =='、'
                    or word =='的' or word == "“" or word == "”" or word == "：" or word == "（" or word == "）" or word == "；" or word == "‘" or word == "’"):
                continue
            elif(re.match('^\s+$',word) != None):
                continue
            else:
                #print(word,i)
                if word in index:
                    index[word].append(i)
                else:
                    index[word] = [i]

print("jieba done.")

#打包
file = open('newspkg','wb+')
pickle.dump(news,file,0)
file.close()

file2 = open('indexpkg','wb+')
pickle.dump(index,file2,0)
file2.close()
print("pickle done.")
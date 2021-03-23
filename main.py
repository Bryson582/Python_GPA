# import requests
# headers = {
#          "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
#             }
# data = {
#     'identity':'1817020105',
#     'password':'19951979kb',
# }
# url ='http://210.30.62.40:8080/jsxsd/xk/LoginToXk'
# session = requests.Session()
# session.post(url,headers = headers,data = data)
# # 登录后，我们需要获取另一个网页中的内容
# response = session.get('http://210.30.62.40:8080/jsxsd/kscj/cjcx_list',headers = headers)
# print(response.status_code)
# print(response.text)
#


# Cookie

import requests
import pandas as pd
from bs4 import BeautifulSoup
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'Cookie':'JSESSIONID=68E5E9087DD3404B3502CD3077A8CDB4',
}
url = 'http://210.30.62.39:8080/jsxsd/xk/LoginToXk'
session = requests.Session()
response = session.get('http://210.30.62.39:8080/jsxsd/kscj/cjcx_list', headers=headers)
df = pd.read_html(response.text)[0]
# 我们需要的一共是三列 第一列是课程名称 第二列是绩点 第三列是学分
# 因为我们需要先对数据进行处理 所以我们可以先把课程名称和绩点作为字典
# key:课程名称 values:字典
column_dict = dict(zip(df['课程名称'],df['学分']))
list1 = ["军事理论与训练","形势与政策","大学生职业生涯与规划","体育1","体育2","体育3","体育4"]
list2 = ["思想道德修养与法律基础","政治经济学","中国近现代史纲要","毛泽东思想和中国特色社会主义理论体系概论","马克思主义基本原理概论","书法鉴赏","道德修养和法律基础","英语口语"]
for key in column_dict.keys():
    if key in list1:
        column_dict[key] = 0.0
    elif key in list2:
        column_dict[key] = 1.0
    elif key in ["大学英语1","大学英语2","大学英语3","大学英语4"]:
        column_dict[key] = 2.0
# print(column_dict)
# 我们修改完学分之后需要对此成绩列做对应 我们可以把学分列取出来 然后和成绩共同组成一个列表
# w为了保证正确 我们可以现判断一下长度是否一致
print(column_dict)
list3 = []
for val in column_dict.keys():
    list3.append(float(column_dict[val]))
# 我们接下来需要根据成绩修正绩点
list4 = []
for tem in df['成绩']:
    if tem in ['优','良','中','合格','及格','不及格']:
        # 此时说我们该项课程的成绩是五级分制
        if tem == "优":
            list4.append(4)
            continue
        elif tem =='良':
            list4.append(3)
            continue
        elif tem =='中':
            list4.append(2)
            continue
        elif tem =='及格' or tem =='合格':
            list4.append(2)
            continue
        else:
            list4.append(0)
            continue
    else:
        tem =  float(tem)
        if tem >= 85:
            list4.append(4)
        elif tem>=75 and tem <= 84:
            list4.append(3)
        elif tem>=60 and tem <=74:
            list4.append(2)
        elif  tem <60:
            list4.append(0)
# print(list4)
# 我们现在已经得到修正过后的绩点列 现在把学分和绩点整合到一个list中
# print(list3)
list_final = [list4,list3]
sum_score=0.0
for i in list3:
    sum_score+=i
print(sum_score)
sum = 0.0
for i in range(0,len(list4)):
    sum += list_final[0][i] * list_final[1][i]
print(sum)
final = float(sum)/float(sum_score)
print(">>>欢迎来到李博文的绩点查询系统>>>")
print(final)

# print(list_final)
# print(list_final[0][0])
# print(list_final[1][0])








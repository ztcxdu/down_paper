# #coding:utf-8
# import requests
# import json
# import re
# import time


# def getArticleInformFromJson():
    # """从json读取文献信息的字典"""
    # with open('paperInformation_((mobile)OR(terminal)OR(phone)OR(handset))AND(antenna).json','r') as f:
        # #print(f.read())
        # paperInform = json.loads(f.read(), strict=False)
    # f.close()
    
    # print(len(paperInform))
    # return paperInform
    
    
    
# def down(paperInform):
    # """下载并保存pdf"""
   # # print(paperIform)
    
    # header = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
    # 'Connection': 'close',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        
    # #cookie = ""
    # for articleNumber in paperInform:
        # print(paperInform[articleNumber][0])
        
        # downLink = paperInform[articleNumber][1]
                
        # #header['Cookie'] = cookie
        # time.sleep(5)
        
        # r = getPaper(downLink)
        
        # fp = open(paperInform[articleNumber][0] + ".pdf", 'wb')
        # fp.write(r.content)
        # fp.close()

# def getPaper(downLink):
    # header = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
    # 'Connection': 'close',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    
    # try:
        # return requests.get(downLink, headers = header, verify =  False)
    # except:
        # time.sleep(5)
        # return getPaper(downLink)

# if __name__ == "__main__":
    # requests.packages.urllib3.disable_warnings()
    # down(getArticleInformFromJson())
    # #getArticleInformFromJson()

import threading
import time
import requests

def T1_job(a):
    print("T1 start")
    print(a)
    for i in range(10):
        time.sleep(0.1)
    print("T1 finish")
    
    
def T2_job(a):
    print('T2 start')
    print(a)
    print('T2 finish')
     
def main():
    #d = {"a":"1","b":"2","c":"3","d":"4"}
    #for i in range(1,len(d)):
       # print(d(1))
    for i in range(1, 101, 3):
        print(i)
        print(i+1)
        print(i+2)
        print("\n")
    #thread1 = threading.Thread(target = T1_job, args = ("hello",))#添加线程
    #thread2 = threading.Thread(target = T1_job, args = ("hello",))
    #thread1.start() #执行添加的线程
    #thread2.start()
    #print(requests.head("https://ieeexplore.ieee.org/ielx7/8/8705603/08649600.pdf?tag=1",headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}).headers)
    
    #thread1.join()
    #thread2.join()
    
    #print('all done\n')
     
if __name__ == "__main__":
    main()

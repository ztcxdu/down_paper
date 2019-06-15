#coding:utf-8
import requests
import json
import re
import time


def getArticleInformFromJson():
    """从json读取文献信息的字典"""
    with open('paperInformation_((mobile)OR(terminal)OR(phone)OR(handset))AND(antenna).json','r') as f:
        #print(f.read())
        paperInform = json.loads(f.read(), strict=False)
    f.close()
    
    #print(len(paperInform))
    return paperInform
    
    
def down(paperInform):
    """下载并保存pdf"""
   # print(paperIform)
    
    header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
    'Connection': 'close',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        
    #cookie = ""
    for articleNumber in paperInform:
        print(paperInform[articleNumber][0])
        
        downLink = paperInform[articleNumber][1]
                
        #header['Cookie'] = cookie
        time.sleep(5)
        
        r = getPaper(downLink)
        
        fp = open(paperInform[articleNumber][0] + ".pdf", 'wb')
        fp.write(r.content)
        fp.close()

def getPaper(downLink):
    header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
    'Connection': 'close',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    
    try:
        return requests.get(downLink, headers = header, verify =  False)
    except:
        time.sleep(5)
        return getPaper(downLink)

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    down(getArticleInformFromJson())
    #getArticleInformFromJson()


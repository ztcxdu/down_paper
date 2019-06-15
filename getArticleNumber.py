#coding:utf-8
import requests
import json
import re
import time
from urllib.parse import parse_qs
from urllib.parse import urlparse


 

class ieeeDownloader(object):
    """一个从ieeexplore批量下载文献的类"""
    
    def __init__(self, downLink):
        self.link = downLink
        self.cookie = ""
        self.searchUrl = 'https://ieeexplore.ieee.org/rest/search'
        self.totalPage = 1
        self.articleNumber = {}
        self.parseResult = {}
        self.queryText = ""
        self.beginPage = 1
        self.endPage = 1
        
        self.fileNameErrorList = ['\u00a0', '\u00b0', '\u00e9', '\u2019', '\u2013', '\u2014', '\u201c','\u201d', '\uff1a', '\\', '/', ':', '*', '?', '"', '<', '>', '|',]
        self.fileNameCorrectLsit = [' ', '.', 'e', "'", '-', '-', "'", "'", ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

        self.webpageHeader = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'close',
        'Host': 'ieeexplore.ieee.org',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        
        self.ajaxHeader = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Origin': 'https://ieeexplore.ieee.org',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'close',
        'Host': 'ieeexplore.ieee.org',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        
        self.initial()

    def initial(self):
        """进行一些初始化"""
        self.getParsed()
        print(self.parseResult) 
        #self.parseResult = '{"action":"search","searchField":"Search_All","matchBoolean":true,"queryText":"((\"Publication Title\":IEEE Transactions on Antennas and Propagation) AND \"Issue\":6)","highlight":true,"returnType":"SEARCH","ranges":["2019_2019_Year"],"returnFacets":["ALL"]}'
        #self.getCookie()
        #self.getSearchResult()
         
        
    def getParsed(self):
        """从下载链接解析出后续需要用到的字典"""
        parsedUrl = urlparse(self.link, allow_fragments = False)
        query = parsedUrl.query
        result = parse_qs(query)
        
        contrastList = ['ranges', 'refinements', 'returnFacets']

        for key in result:
            if key in contrastList:
                self.parseResult[key] = result[key]
            else:
                self.parseResult[key] = result[key][0]
            
        self.queryText = self.parseResult['queryText']

    # def getCookie(self):
        # """搜索页必须有cookie，故先获取一个cookie"""
        # url = 'https://ieeexplore.ieee.org/Xplore/home.jsp'
        # re = requests.get(url, headers =  self.webpageHeader)
        # ##self.cookie = re.headers['Set-Cookie']
        
    def getSearchResult(self):
        """获取总的页码信息"""
        url = downLink
        header1 = self.webpageHeader
        
        ##header1['Cookie'] = self.cookie
        
        rsp = requests.get(url, headers = header1)

        ##self.cookie = rsp.headers['Set-Cookie']
        
        header2 = self.ajaxHeader
        ##header2['Cookie'] = self.cookie
        rsp = requests.post(self.searchUrl, headers = header2, data = json.dumps(self.parseResult))
        
        ##self.cookie = rsp.headers['Set-Cookie']
        
        paperInform = json.loads(rsp.text)
        self.totalPage = paperInform['totalPages']
        
        
    def getDifferentPage(self, page):
        """获取每页的文献信息"""
        print("Getting the " + str(page) + "th page")
        header = self.ajaxHeader
        ##header['Cookie'] = self.cookie
        
        #request_payload = {"queryText":"((phone) OR (terminal)) AND (antenna)","highlight":'true',"returnType":"SEARCH","sortType":"oldest","returnFacets":["ALL"],"ranges":["2009_2019_Year"],"refinements":["PublicationTitle:IEEE Transactions on Antennas and Propagation","PublicationTitle:IEEE Antennas and Wireless Propagation Letters","PublicationTitle:IEEE Access"],"pageNumber":page}
        requestPayload = self.parseResult
        requestPayload['pageNumber'] = page

        rsp = requests.post(self.searchUrl, headers = header, data = json.dumps(requestPayload))
        
        try:
            self.cookie = rsp.headers['Set-Cookie']
        except:
            pass
            
        paperInform = json.loads(rsp.text)
        self.totalPage = paperInform['totalPages']
        
        for paper in paperInform['records']:
            paper['articleTitle'] = self.correctFileName(paper['articleTitle'])
            print(paper['articleNumber'] + ' ' + paper['articleTitle'])

            paperNameDownLink = [paper['articleTitle']]
            time.sleep(5)
            paperNameDownLink.append(self.getDownLink(paper['articleNumber']))

            self.articleNumber[paper['articleNumber']] = paperNameDownLink
        
        self.writeResult()

    def controlPage(self):
        """控制获取的页数"""
        #print("There are " + str(self.totalPage) + " page(s) in the result")
        self.beginPage = int(input("Input the begin page of the range you want to download:"))
        self.endPage = int(input("Input the last page of the range you want to download:"))
        for page in range(self.beginPage, self.endPage + 1):
        #for page in range(2, self.totalPage):
            self.getDifferentPage(page)


    def writeResult(self):
        """将获取的文献信息的字典写入json文件"""
        
        try:
            with open("paperInformation_" + self.queryText + ".json", 'r') as fp:
                paperInformPrevious = json.loads(fp.read(), strict=False)
                fp.close()
        except:
            paperInformPrevious = {}
            
        with open("paperInformation_" + self.queryText + ".json", 'w') as fp:
            json.dump(dict( paperInformPrevious, **self.articleNumber ), fp)
            fp.close()
        self.articleNumber = {}
        
    def correctFileName(self, articleTitle):
        """对文件名中windows不支持的字符进行替换"""
        for i in range(0, len(self.fileNameErrorList)):
            if self.fileNameErrorList[i] in articleTitle:
                articleTitle = articleTitle.replace(self.fileNameErrorList[i], self.fileNameCorrectLsit[i])
        
        return articleTitle
         
    def getDownLink(self, articleNumber):
        """获取下载链接"""
        url = 'https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=' + articleNumber
        
        header = self.webpageHeader
        #header['Cookie'] = self.cookie
        try:
            rsp1 = requests.get(url, headers = header,timeout = 30)
        except:
            return self.getDownLink(articleNumber)

        try:
            self.cookie = rsp1.headers['Set-Cookie']
            #header['Cookie'] = self.cookie
        except:
            pass

        print('1')
        downLink = re.findall('https://ieeexplore.ieee.org/\S*.pdf', rsp1.text)
        
        if downLink == []:
            print('2')
            rsp2 = requests.get(url + "&tag=1", headers = header)

            try:
                self.cookie = rsp2.headers['Set-Cookie']
            except:
                pass
            
            downLink = re.findall('https://ieeexplore.ieee.org/\S*.pdf', rsp2.text)
        
        if downLink == []:
            self.cookie = ""
            print("Sleep for 30 seconds to avoid too frequent operation")
            time.sleep(30)
            return self.getDownLink(articleNumber)
        else:
            return downLink[0]
    
    def downPaper(self, paperInform):
        """下载并保存pdf"""
        for articleNumber in paperInform:
            print(paperInform[articleNumber][0])
        
            downLink = paperInform[articleNumber][1]
                
            r = requests.get(downLink, headers = self.webpageHeader)
            fp = open(paperInform[articleNumber][0] + ".pdf", 'wb')
            fp.write(r.content)
            fp.close()


    
if __name__ == "__main__":
    
    downLink = input("Input the search link:")
    downloader = ieeeDownloader(downLink)
    downloader.controlPage()
    
    

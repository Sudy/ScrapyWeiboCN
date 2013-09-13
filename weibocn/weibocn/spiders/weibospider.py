#!/usr/bin/env python
#-*- encoding=utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from weibocn.items import WeibocnItem,CmtRptItem
from scrapy.http import Request
import re

class WeibocnSpider(CrawlSpider):
    name = 'weibo'
    allowed_domains = ['weibo.cn']

    def __init__(self):
        super(WeibocnSpider,self).__init__()

        '''
        rules = (
            # Extract links matching 'category.php' (but not matching 'subsection.php')
            # and follow links from them (since no callback means follow=True by default).
            Rule(SgmlLinkExtractor(allow=('http://weibo\.cn/u/[0-9]{10}\?'),callback='parse_weibo')),

            # Extract links matching 'item.php' and parse them with the spider's method parse_item
            Rule(SgmlLinkExtractor(allow=('http://weibo\.cn/repost/[A-Za-z0-9]{3,9}', )), callback='parse_repost'),
            Rule(SgmlLinkExtractor(allow=('http://weibo\.cn/comment/[A-Za-z0-9]{3,9}', )), callback='parse_comment'),
        )
        '''

        self.repost_pattern = re.compile("http://weibo.cn/repost/([A-Za-z0-9]{3,9})")
        self.comment_pattern = re.compile("http://weibo.cn/comment/([A-Za-z0-9]{3,9})")
        self.uid_pattern = re.compile("http://weibo.cn/u/([0-9]{10})")

        self.accountlist = list()
        self.urllist = list()

    def start_requests(self):
        self.initSeed()
        self.initAccount()
        for i in range(0,len(self.urllist)-1):
            url = self.urllist[i] + self.accountlist[i]
            self.log(url)
            yield Request(url=url,callback=self.parse_weibo)


    def initSeed(self):
        #get all the available seed
        fp = open("seed","r")
        #open the seed list
        line = fp.readline()
        
        while "" != line and not line.startswith("#"):
            strurl = "http://weibo.cn/u/" + line + "?vt=4&gsid="
            self.urllist.append(strurl)    
            line = fp.readline()
        fp.close()
 

    def initAccount(self):
        
        fp = open("account","r")

        #open the seed list
        line = fp.readline()
        
        while "" != line and not line.startswith("#"):
            self.accountlist.append(line)    
            line = fp.readline()
        fp.close()
        
    def parse_weibo(self,response):
        hxs = HtmlXPathSelector(response)

        uid = self.uid_pattern.match(response.url).group(1)

        weibos = hxs.select("//div[@class='c']")

        for weibo in weibos:
            wbItem = WeibocnItem()
            wbItem['uid'] = uid  
            wbItem['mid'] = weibo.select("/@id").re("M_([A-Za-z0-9]{3,9})")
            wbItem['cnt'] = weibo.select("/div/span[@class='ctt']//text()").extract()
            wbItem['like'] = weibo.select("/div[last()]/a[position() = last()- 3]/text()").extract()
            wbItem['repost'] = weibo.select("/div[last()]/a[position() = last()- 2]/text()").extract()
            wbItem['cmt'] = weibo.select("/div[last()]/a[position() = last()- 1]/text()").extract()
            wbItem['time'] = weibo.select("/div/span[@class='ct']/text()").extract()
            yield wbItem
            yield Request(url = weibo.select("/div[last()]/a[position() = last()- 2]/@href").extract(),\
                callback = self.parse_repost)
            yield Request(url = weibo.select("/div[last()]/a[position() = last()- 1]/@href").extract(),\
                callback = self.parse_comment)




    def parse_comment(self,response):
        hxs = HtmlXPathSelector(response)
        #//div[@class='c']/span[@class='ctt']//text()
        comments = hxs.select("//div[@class='c']")
        #comment
        #message id, user name,nickname
        #content,time and type
        mid = self.comment_pattern.match(response.url).group(1)
        #mid = hxs.select("//div[@class='c'][1]/@id").re("M_([A-Za-z0-9]{3,9})")
        for comment in comments:
            crItem = CmtRptItem()
            crItem["mid"] = mid
            crItem["usrname"] = comment.select("/a[1/@href").re('(.*?)\?vt')
            crItem["nickname"] = comment.select("/a[1]/text()").extract() 
            crItem["cnt"] = comment.select("/span[@class='ctt']//text()").extract()
            crItem["time"] = comment.select("/span[@class='ct']/text()").extract()
            crItem["tid"] = 1
            yield crItem

    def parse_repost(self,response):
        hxs = HtmlXPathSelector(response)

        mid = self.repost_pattern.match(response.url).group(1)
        #mid = hxs.select("//div[@class='c'][1]/@id").re("M_([A-Za-z0-9]{3,9})")
        #//div[@class='c']//text()[not(parent::span) and not(parent::a)]
        reposts = hxs.select("//div[@class='c'][position() > 2]")
        
        for repost in reposts:
            crItem = CmtRptItem()
            crItem["mid"] = mid
            crItem["usrname"] = repost.select("/a[1]/@href").re('(.*?)\?vt')
            crItem["nickname"] = repost.select("/a[1]/text()").extract() 
            crItem["cnt"] = repost.select("//text()[not(parent::span)]").extract()[1:]
            crItem["time"] = repost.select("/span[@class='ct']/text()").extract()
            crItem["tid"] = 2
            yield crItem

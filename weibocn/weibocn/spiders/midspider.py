#!/usr/bin/env python
#-*- encoding=utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from weibocn.items import MidItem
from scrapy.http import Request

class MidSpider(CrawlSpider):
    name = 'midspider'
    allowed_domains = ['weibo.cn']

    rules = (
            # Extract links matching ’category.php’ (but not matching ’subsection.php’)
            # and follow links from them (since no callback means follow=True by default).
            Rule(SgmlLinkExtractor(allow=('http://weibo.cn/u/.*?',))),
        )


    def __init__(self):
        super(MidSpider,self).__init__()

        self.accountlist = list()
        self.urllist = list()

    def start_requests(self):
        self.initSeed()
        self.initAccount()
        for i in range(0,len(self.urllist)-1):
            url = self.urllist[i] + self.accountlist[i]
            yield Request(url=url,callback=self.parse_weibo)


    def initSeed(self):
        #get all the available seed
        fp = open("seed","r")
        #open the seed list
        line = fp.readline()
        
        while "" != line and not line.startswith("#"):
            strurl = "http://weibo.cn/u/" + line.strip() + "?vt=4&gsid="
            self.urllist.append(strurl)    
            line = fp.readline()
        fp.close()
 

    def initAccount(self):
        
        fp = open("account","r")

        #open the seed list
        line = fp.readline()
        
        while "" != line and not line.startswith("#"):
            self.accountlist.append(line.strip())    
            line = fp.readline()
        fp.close()
        
    def parse_weibo(self,response):
        hxs = HtmlXPathSelector(response)
        weibos = hxs.select("//div[@class='c']/@id").extract()

        appendix = hxs.select("//div[@class='pa']//a/@href").extract()[0]
        url = "http://weibo.cn" + appendix
        yield Request(url=url,callback=self.parse_weibo)
        
        for weibo in weibos:
            midItem = MidItem()
            midItem["mid"] = weibo.replace("M_","")
            yield midItem
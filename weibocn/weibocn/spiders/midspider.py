#!/usr/bin/env python
#-*- encoding=utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from weibocn.items import WeibocnItem
from scrapy.http import Request
import time
import base62
import re

class WeiboCNSpider(CrawlSpider):
    name = 'weibospider'
    allowed_domains = ['weibo.cn']

    rules = (
            # Extract links matching ’category.php’ (but not matching ’subsection.php’)
            # and follow links from them (since no callback means follow=True by default).
            Rule(SgmlLinkExtractor(allow=('http://weibo.cn/u/.*?',)),callback='parse_weibo'),
            Rule(SgmlLinkExtractor(allow=('http://weibo.cn/comment/.*?',)),callback='parse_comment'),
        )


    def __init__(self):
        super(WeiboCNSpider,self).__init__()
        #self.start_time = time.mktime(time.strptime("2013-01-23","%Y-%m-%d"))
        self.start_time = time.mktime(time.strptime("2013-01-23","%Y-%m-%d"))

        self.uid_pattern = re.compile("/([a-z0-9]+)\?")
        self.mid_pattern = re.compile("/([a-zA-Z0-9]+)\?")

        self.accountlist = list()
        self.urllist = list()

    def start_requests(self):
        self.initSeed()
        self.initAccount()
        account_num = len(self.accountlist)
        for i in range(0,len(self.urllist)):
            url = self.urllist[i] + self.accountlist[i%account_num]
            self.log(url)
            yield Request(url=url,callback=self.parse_weibo)
    
    def initSeed(self):
        #get all the available seed
        fp = open("/home/owen/workspace/ScrapyWeiboCN/weibocn/weibocn/spiders/2-2013-02-23.txt","r")
        #open the seed list
        line = fp.readline()
        
        while "" != line and not line.startswith("#"):
            uid_page = line.strip().split()
            strurl = "http://weibo.cn/u/" + uid_page[0] + "?page=" + uid_page[1] + "&vt=4&gsid="
            self.urllist.append(strurl)    
            line = fp.readline()
        fp.close()
 
    
    def initAccount(self):
        
        fp = open("/home/owen/workspace/ScrapyWeiboCN/weibocn/weibocn/spiders/account","r")

        #open the seed list
        line = fp.readline()
        
        while "" != line and not line.startswith("#"):
            self.accountlist.append(line.strip())    
            line = fp.readline()
        fp.close()

    def parse_weibo(self,response):
        hxs = HtmlXPathSelector(response)

        try:
            #get post uid
            uid = ""
            uid_match = self.uid_pattern.search(response.url)
            if uid_match != None:
                uid = uid_match.group(1)
            else:
                return
            
            #get weibo content
            weibos = hxs.select("//div[@class='c']")

            for weibo in weibos:
                try:
                    #get the post time
                    weiboItem = WeibocnItem()

                    post_time_text = weibo.select('div/span[@class="ct"]/text()').extract()[0]
                    weiboItem['time'] = post_time_text.strip()#.rsplit(" ",1)[0]
                    #if post time is earlies than the event starts
                    #ignore it
                    try:
                        post_time = time.mktime(time.strptime(u"2013-" + post_time_text.split(" ",1)[0].strip(),u"%Y-%m月%d日"))
                        
                        if post_time < self.start_time:
                            return
                    except:
                        continue
                    
                    weiboItem['mid'] = base62.url_to_mid(weibo.select("@id").re("M_([a-zA-Z0-9]+)")[0])
                    weiboItem['uid'] = uid
                    weiboItem['cnt'] = weibo.select('div[1]/span[((@class="cmt") and (position()=1)) or (@class="ctt")]//text() ').extract()
                    weiboItem['tid'] = 1
                    weiboItem['eid'] = 2
                    yield weiboItem

                    #get comment page
                    comment_url = weibo.select('div[last()]/a[last()-1]/@href').extract()[0]
                    self.log(comment_url)
                    yield Request(url=comment_url,callback=self.parse_comment)
                except:
                    continue
            #next page
            appendix = hxs.select("//div[@class='pa']//a/@href").extract()[0]
            url = "http://weibo.cn" + appendix
            yield Request(url=url,callback=self.parse_weibo)

        except:
            self.log(response.url)


    def parse_comment(self,response):
        

        hxs = HtmlXPathSelector(response)

        try:
            comments =  hxs.select('//div[@class="c"]')
            #mid of the weibo
            mid = self.mid_pattern.search(response.url).group(1)

            #comment content
            for comment in comments:
                try:
                    commentItem = WeibocnItem()
                    commentItem['mid'] = base62.url_to_mid(mid)
                    uid_raw = comment.select('a/@href').extract()[0]
                    commentItem['uid'] = self.uid_pattern.search(uid_raw).group(1) 
                    commentItem['cnt'] = comment.select('span[@class="ctt"]//text()').extract()
                    commentItem['time'] = comment.select('span[@class="ct"]/text()').extract()[0].strip()#.rsplit(" ",1)[0]
                    commentItem['tid'] = 2
                    commentItem['eid'] = 2
                    yield commentItem
                except:
                    continue

            #get next page
            next_page_url = hxs.select('//div[@class="pa"]//a/@href').extract()[0]
            self.log("-------------http://weibo.cn" + next_page_url)
            yield Request(url="http://weibo.cn" + next_page_url,callback=self.parse_comment)
        except:
            pass
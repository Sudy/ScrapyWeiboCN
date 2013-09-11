#!/usr/bin/env python
#-*- encoding=utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item

class WeibocnSpider(CrawlSpider):
    name = 'weibo.cn'
    allowed_domains = ['weibo.cn']


    start_urls = [
					'http://weibo.cn/u/?vt=4',

    ]

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(SgmlLinkExtractor(allow=('http://weibo\.cn/u/[0-9]{10}\?'),callback='parse')),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(SgmlLinkExtractor(allow=('http://weibo\.cn/comment/', )), callback='parse_item'),
    )
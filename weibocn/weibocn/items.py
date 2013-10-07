# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class WeibocnItem(Item):
    # define the fields for your item here like:
    # name = Field()
    #userid,message id,content,like,repost,and comment
    mid = Field()
    uid = Field()
    cnt = Field()
    pos = Field()
    time = Field()
    tid = Field()
    #event id
    eid = Field()

'''
#comment and repost item
class CmtRptItem(Item):
    #message id, user name,nickname
    #content,time and type
    mid = Field()
    uid = Field()
    cnt = Field()
    pos = Field()
    time = Field()

#comment and repost item
class MidItem(Item):
    #message id, user name,nickname
    #content,time and type
    mid = Field()
'''
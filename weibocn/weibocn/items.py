# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class WeibocnItem(Item):
    # define the fields for your item here like:
    # name = Field()
    #userid,message id,content,like,repost,and comment
    uid = Field()
    mid = Field()
    cnt = Field()
    like = Field()
    repost = Field()
    cmt = Field()
    time = Field()

#comment and repost item
class CmtRptItem(Item):
    #message id, user name,nickname
    #content,time and type
    mid = Field()
    usrname = Field()
    nickname = Field()
    cnt = Field()
    time = Field()
    tid = Field()

#comment and repost item
class MidItem(Item):
    #message id, user name,nickname
    #content,time and type
    mid = Field()
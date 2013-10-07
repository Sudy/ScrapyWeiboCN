# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
#from scrapy.core.exceptions import DropItem
from twisted.enterprise import adbapi

import time
import MySQLdb.cursors

class WeibocnPipeline(object):

    def __init__(self):
        # @@@ hardcoded db settings
        # TODO: make settings configurable through settings
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                db='weibodata',
                user='root',
                passwd='123456',
                cursorclass=MySQLdb.cursors.DictCursor,
                charset='utf8',
                use_unicode=True
            )

    def process_item(self, item, spider):
        # run db query in thread pool

        if len(item["cnt"]) == 0 or len(item["time"]) == 0:
            return


        content = ""
        for cnt in item["cnt"]:
            content += cnt.strip()
        if "" != content:
            item["cnt"] = content
        else:return

        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)

        #return item

    def _conditional_insert(self, tx, item):
        # create record if doesn't exist. 
        # all this block run on it's own thread

        try:
            tx.execute(\
                "insert into event_data (mid, uid, cnt, time,tid,eid) "
                "values (%s, %s, %s, %s, %s, %s)",
                (
                 item['mid'],
                 item['uid'],
                 item['cnt'],
                 item['time'],
                 item['tid'],
                 item['eid'],
                 )
            )
            log.msg("Item stored in db: %s" % item["mid"], level=log.DEBUG)
        except:
            log.msg("insert %s error" % item,level=log.ERROR)

    def handle_error(self, e):
        log.err(e)

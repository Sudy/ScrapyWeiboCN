# Scrapy settings for weibocn project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'weibocn'

SPIDER_MODULES = ['weibocn.spiders']
NEWSPIDER_MODULE = 'weibocn.spiders'
DEFAULT_ITEM_CLASS = 'weibocn.items.WeibocnItem'
ITEM_PIPELINES = ['weibocn.pipelines.WeibocnPipeline']
SCHEDULER_ORDER = 'DFO'
CONCURRENT_REQUESTS = 50

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'weibocn'
DOWNLOAD_DELAY = 2
DOWNLOAD_TIMEOUT = 5

# Specify the host and port to use when connecting to Redis (optional).
REDIS_HOST = '192.168.3.48'
REDIS_PORT = 6379


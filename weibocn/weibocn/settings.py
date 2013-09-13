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
SCHEDULER_ORDER = 'BFO'
CONCURRENT_REQUESTS = 32
# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'weibocn'
DOWNLOAD_DELAY = 3
DOWNLOAD_TIMEOUT = 15


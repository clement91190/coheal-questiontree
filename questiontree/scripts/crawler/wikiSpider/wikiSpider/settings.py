# Scrapy settings for wikiSpider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'wikiSpider'

SPIDER_MODULES = ['wikiSpider.spiders']
NEWSPIDER_MODULE = 'wikiSpider.spiders'
DEPTH_LIMIT = 1
DOWNLOAD_DELAY = 0.5 
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'wikiSpider (+http://www.yourdomain.com)'

# -*-coding:Utf-8 -*
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

class wikiSpider(CrawlSpider):
    name = "wikiSpider"
    allowed_domains = ['wikipedia.org']
    start_urls = ["http://en.wikipedia.org/wiki/Medicine"]

    rules = (
    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="mw-body"]//a/@href'))),
    Rule(SgmlLinkExtractor( allow=("http://en.wikipedia.org/wiki/",)), callback='parse_item'),
    )


    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        items = hxs.select('//a/text()').extract()
        for i in items: 
            print i

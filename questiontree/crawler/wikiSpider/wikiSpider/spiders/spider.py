# -*-coding:Utf-8 -*
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
import nltk


class wikiSpider(CrawlSpider):
    name = "wikiSpider"
    allowed_domains = ['wikipedia.org']
    symptome_list = ['cyanose', 'attaque de panique']
    #start_urls = ["http://fr.wikipedia.org/wiki/Medecine"]
    start_urls = []
    for s in symptome_list:
        start_urls.append('https://www.google.fr/search?sclient=psy&hl=fr&source=hp&q=' + s.encode('UTF-8') + '&btnG=Rechercher'
                +'#q='+ s.encode('UTF-8'))
    """    
    rules = (
    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="mw-body"]//a/@href'))),
    Rule(SgmlLinkExtractor( allow=("http://fr.wikipedia.org/wiki/",)), callback='parse_item'),
    )
"""
    rules = (
    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@id="center_col"]/li[@class="g"]/h3[@class="r"]/a/@href'))),
    Rule(SgmlLinkExtractor( allow=("",)), callback='parse_item'),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        items = hxs.select('//div[@id="bodyContent"]//text()').extract()
        with open('data.txt', 'w+') as fich:
            for i,v in enumerate(items):
                #items[i] = unicodedata.normalize('NFKC', v)
                tag = v.encode('UTF-8')
                tokens = nltk.word_tokenize(tag)   
                for t in tokens:
                    if len(t) > 6:
                        fich.write(t)
                        fich.write('\n')
            #print "chose vues ici{}".format(items)

# -*-coding:Utf-8 -*
import urllib2
from HTMLParser import HTMLParser
import nltk
import traceback
import chardet
import re
import questiontree.db.models as models


class HTMLParserdepth(HTMLParser):
    def handle_starttag(self, tag, attrs):
        pass
    
    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        words = nltk.word_tokenize(data)
        tags = nltk.pos_tag(words)
        with open('data.txt', 'a+') as fich:
            for w, t in tags:
                if t.find('NN') >= 0 and len(w) > 6 and re.match("^[A-Za-z]*$", w):
                    fich.write(w)
                    #print w, t
                    fich.write('\n')


class MyHTMLParser(HTMLParser):
   
    def __init__(self, l):
        HTMLParser.__init__(self)
        self.cursor = 0
        self.search_list = l
        self.use_data = False
        self.depth = []
        self.links = []
    
    def google_link(self, str):
        return str[7:str.find('&sa')]

    def handle_starttag(self, tag, attrs):
        if self.cursor >= len(self.search_list): 
            self.use_data = True
            #print "use this tag", tag
            try:
                link = self.google_link(dict(attrs)['href']) 
                print "use this link {}".format(link)
                self.links.append(link)
            except:
                pass
        else: 
            self.use_data = False
           
            if tag == self.search_list[self.cursor][0]:
                att = self.search_list[self.cursor][1]
                if all([dict(attrs).get(k, False) == v for k, v in att]):
                    self.cursor += 1
                    self.depth.append(1)
                    #print "{} and {} found".format(tag, attrs)
                else:
                    pass
                    #print "{} found but wrong {} , {}".format(tag, attrs, att)
            elif self.cursor > 0 and tag == self.search_list[self.cursor - 1][0]:
                self.depth[-1] += 1
    
    def handle_endtag(self, tag):
        if self.cursor > 0 and tag == self.search_list[self.cursor - 1][0]:
            self.depth[-1] -= 1
            if self.depth[-1] == 0:
                self.depth.pop()
                self.cursor -= 1
                #print "fin de {}".format(tag)

    def handle_data(self, data):
        if self.use_data:
            #print "use this data:", data
            pass


def google_format(key):
    while key.find(" ") >= 0:
        ind = key.find(" ")
        key= key[:ind] + '%20' + key[ind+1:]
    return key    

def search(key):
    #url = 'https://www.google.com?q=' + key + '#q=' + key
    #result = urllib2.urlopen(url)
    request = urllib2.Request('')
    request_headers = {'User-Agent': 'MyBrowser/0.1'}
    url = 'http://www.google.com/search?q={}'.format(google_format(key))  
    print "Google search for {}".format(url)
    request = urllib2.Request(url, None, request_headers)
    result = urllib2.urlopen(request)
    return result


def get_links(key):
    res = search(key).read()
    #print res
    l = [('html', []), ('body', []), ('div', [('id', 'center_col')]),
         ('li', [('class', 'g')]), ('h3', [])]
    parser = MyHTMLParser(l)
    parser.feed(res)
    return parser.links


def crawl(key):
    links = get_links(key)
    parser = HTMLParserdepth()
    for l in links:
        print "[crawling] link {} ".format(l)
        try:
            result = urllib2.urlopen(l)
            page = result.read()
            try:
                encoding = result.headers.getparam('charset')
                page = page.decode(encoding)
                parser.feed(page)   
            except UnicodeDecodeError:
                encoding = chardet.detect(page)['encoding']
                if encoding != 'unicode':
                    page = page.decode(encoding)
                    page = page.encode('ascii', 'ignore')
                    parser.feed(page)
                    print 'success'        
            except:
                #traceback.print_exc()
                pass
        except:
            #traceback.print_exc()
            print " BAD LINK : {}".format(l)
    

def main():
    crawl('medecine')
    l = models.Question.get_all_symptome()
    print l 
    for s in l:
        print s
        crawl(s.encode('UTF-8'))

if __name__ == "__main__":
    main()

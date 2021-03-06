# -*-coding:Utf-8 -*
import urllib2
from HTMLParser import HTMLParser
import nltk
import traceback
import chardet
import re
import questiontree.db.models as models

""" The aim of this file is to crawl webpage from google search, 
so that we can find tags and build a graph of relations between this tags. """


class HTMLParserdepth(HTMLParser):
    """ Parser for the webpages coming from different links from google"""
    def __init__(self):
        HTMLParser.__init__(self)
        """ list of tags encoutered by the parser"""
        self.tags = []

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
                    self.tags.append(w)
                    #print w, t
                    #fich.write('\n')


class MyHTMLParser(HTMLParser):
    """general crawler for any html file, use a list l of 
    html tags to find the links in the page"""
    def __init__(self, l):
        HTMLParser.__init__(self)
        self.cursor = 0
        self.search_list = l
        self.use_data = False
        self.depth = []
        self.links = []
    
    def google_link(self, str):
        """ get the real link from google links"""
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
    """ change the keyword to replace certain character in the google 
    search ( for instance spaces)"""
    while key.find(" ") >= 0:
        ind = key.find(" ")
        key= key[:ind] + '%20' + key[ind+1:]
    return key    


def search(key):
    """function to run a search on google and return
    the html file"""
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
    """ return the links return by the search """
    res = search(key).read()
    #print res
    l = [('html', []), ('body', []), ('div', [('id', 'center_col')]),
         ('li', [('class', 'g')]), ('h3', [])]
    parser = MyHTMLParser(l)
    parser.feed(res)
    return parser.links


def build_graph_relations_from_tag_list(tags, tag_dict):
    """ look in the tags returned if to of them are in the 
    database, and if they are, add the relation """
    print " ### building relations ###"
    print " length : {}".format(len(tags))
    for t1 in tags:
        print t1
        for t2 in tags:
            if t1 in tag_dict.keys() and t2 in tag_dict.keys():
                id1 = tag_dict[t1].tag_id
                id2 = tag_dict[t2].tag_id
                print "[ADD] ajout d'arrete"
                try:
                    try:
                        tag_dict[t1].edges[id2] += 1
                    except:
                        tag_dict[t1].edges = {}
                        tag_dict[t1].edges[id2] = 1
                    try:
                        tag_dict[t2].edges[id1] += 1
                    except:
                        tag_dict[t2].edges = {}
                        tag_dict[t2].edges[id1] = 1
                except:
                    print " NOT GOOD"
                    traceback.print_exc()


def crawl(key, buildGraph=False, all_tags=[]):
    """ crawl the result of the search based on the key"""
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
                if buildGraph:
                    build_graph_relations_from_tag_list(parser.tags, all_tags)
                    parser.tags = []
            except UnicodeDecodeError:
                encoding = chardet.detect(page)['encoding']
                if encoding != 'unicode':
                    page = page.decode(encoding)
                    page = page.encode('ascii', 'ignore')
                    parser.feed(page)
                    if buildGraph:
                        print "LA"
                        build_graph_relations_from_tag_list(parser.tags, all_tags)
                        parser.tags = []
                    print 'success'        
            except:
                print "##########ERROR#########"
        except:
            traceback.print_exc()
            print " BAD LINK : {}".format(l)
    

def build_tag_list():
    crawl('medecine')
    l = models.Question.get_all_symptome()
    print l 
    for s in l:
        print s
        crawl(s.encode('UTF-8'))


def build_graph():
    print "BUILDING GRAPH"
    all_tags = models.Tag.objects(banned__ne=True)
    d = {t.text: t for t in all_tags}
    crawl('medecine', True, d)
    l = models.Question.get_all_symptome()
    for s in l:
        print s
        crawl(s.encode('UTF-8'), True, d)
    for t in all_tags:
        t.save()


def main():
    build_graph()


if __name__ == "__main__":
    main()

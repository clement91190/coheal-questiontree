import urllib2
from HTMLParser import HTMLParser
import re

class MyHTMLParser(HTMLParser):
   
    def __init__(self, l):
        HTMLParser.__init__(self)
        self.cursor = 0
        self.search_list = l
        self.use_data = False
        self.depth = []

    def handle_starttag(self, tag, attrs):
        if self.cursor >= len(self.search_list): 
            self.use_data = True
            print "use this tag", tag
        else: 
            self.use_data = False
           
            if tag == self.search_list[self.cursor][0]:
                att = self.search_list[self.cursor][1]
                if all([dict(attrs).get(k, False) == v for k,v in att]):
                    self.cursor += 1
                    self.depth.append(0)
                    print "{} and {} found".format(tag, attrs)
                else:
                    pass
                    #print "{} found but wrong {} , {}".format(tag, attrs, att)
            elif self.cursor > 0 and tag == self.search_list[self.cursor - 1][0]:
                self.depth[-1] += 1
    
    def handle_endtag(self, tag):
        if self.cursor > 0 and tag == self.search_list[self.cursor - 1][0]:
            self.cursor -= 1
            self.depth[-1] -= 1
            if self.depth[-1] == 0:
                self.depth.pop()
                self.cursor -= 1
            print "fin de {}".format(tag)
    
    def handle_data(self, data):
        if self.use_data:
            #print "use this data:", data
            pass


def search(key):
    #url = 'https://www.google.com?q=' + key + '#q=' + key
    #result = urllib2.urlopen(url)
    request = urllib2.Request('')
    request_headers = { 'User-Agent': 'MyBrowser/0.1' }
    request = urllib2.Request('http://www.google.com/search?q=' + key , None, request_headers)
    result = urllib2.urlopen(request)

    return result


def get_links(key):
    res = search(key).read()
    #print res
    l = [('html', []), ('body', []), ('div', [('id', 'center_col')]),
            ('li', [('class', 'id')])]
    parser = MyHTMLParser(l)
    parser.feed(res)


def main():
    get_links('truc')


if __name__ == "__main__":
    main()

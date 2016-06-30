from BeautifulSoup import BeautifulSoup
from urllib import urlopen
bs=BeautifulSoup(urlopen('https://twitter.com/search?f=tweets&vertical=default&q=%23LBint&src=typd'), convertEntities=BeautifulSoup.HTML_ENTITIES)
for l in bs.find('div',{'class':'stream'}).findAll('li'):
    if l.find('p'):
        print l.find('p').text.encode('utf-8')
from BeautifulSoup import BeautifulSoup
from urllib import urlopen
bs=BeautifulSoup(urlopen('https://twitter.com/LBKanzez/with_replies'), convertEntities=BeautifulSoup.HTML_ENTITIES)
for l in bs.find('div',{'class':'stream'}).findAll('li'):
    if l.find('p'):
        print l.find('p').text.encode('utf-8')
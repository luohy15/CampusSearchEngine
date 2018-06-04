from bs4 import BeautifulSoup
import urllib.request
import re
from urllib.parse import urljoin
 
def links_from_html(body, url):
    soup = BeautifulSoup(body)
    res = []
    for link in soup.findAll('a', attrs={'href': re.compile("^")}):
        #  print(link.get('href'))
        res.append(urljoin(url, link.get('href')))
    return res


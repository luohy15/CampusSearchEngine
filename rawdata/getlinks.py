from bs4 import BeautifulSoup
import urllib.request
import re
from urllib.parse import urljoin
 
def links_from_html(body):
    soup = BeautifulSoup(body)
    res = []
    for link in soup.findAll('a', attrs={'href': re.compile("^")}):
        #  print(link.get('href'))
        #  print(type(urljoin("http://master.pbcsf.tsinghua.edu.cn", link.get('href'))))
        res.append(urljoin("http://master.pbcsf.tsinghua.edu.cn", link.get('href')))
    return res


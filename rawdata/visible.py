from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(soup, fid):
    #  if soup.title:
        #  if soup.title.string:
            #  print(soup.title.string.replace("\n", ""))
        #  else:
            #  print("")
    #  else:
        #  print("")
    texts = soup.findAll(text=True)
    texts = filter(lambda t : False if t == '\n' else True, texts)
    visible_texts = filter(tag_visible, texts)
    res = u" ".join(t.strip() for t in visible_texts)
    res = res.replace("\n", "")
    #  if (fid == 793):
        #  print("soup:", soup)
        #  print("text:", list(texts))
        #  print("visible_texts:", res)
    #  if res == "":
        #  res = " "
    return res


if __name__ == "__main__":
    #  tr = urllib.request.urlopen("http://cfrc.pbcsf.tsinghua.edu.cn/index.php?l=en.html").read()
    data_path = "/Users/rv/src/project/search_engine/rawdata"
    link = "http://master.pbcsf.tsinghua.edu.cn/content/details303_13197.html"
    fp = data_path + link[6:]
    print(fp)
    #  url = "http://" + fp[len(data_path)+1:];
    #  print(url)
    with open(fp, "r") as fin:
        tr = fin.read()
        print(text_from_html(tr, 793))

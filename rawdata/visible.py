from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body, fid):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    texts = filter(lambda t : False if t == '\n' else True, texts)
    visible_texts = filter(tag_visible, texts)
    res = u" ".join(t.strip() for t in visible_texts)
    res = res.replace("\n", "")
#    if (fid == 264):
#        print("soup:", soup)
#        #  print("text:", list(texts))
#        print("visible_texts:", res)

    return res


if __name__ == "__main__":
    tr = urllib.request.urlopen("http://www.tsinghua.edu.cn/publish/cs/8212/index.html").read()
    text_from_html(tr, 264)

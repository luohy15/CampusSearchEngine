import sys
import os
from bs4 import BeautifulSoup
from visible import *
from getlinks import *

file2id = {}
out = {}

def get_id(s):
    if s in file2id:
        return file2id[s]
    else:
        file2id[s] = len(file2id) + 1
        out[file2id[s]] = []
    return file2id[s]

def build_fileid():
    for root, dirs, files in os.walk("."): 
        for fi in files:
            print(",", end="")
            sys.stdout.flush()
            get_id(root+"/"+fi)

def parse_files():
    for root, dirs, files in os.walk("."): 
        #  i = 0
        for fi in files:
            #  i = i + 1
            #  if (i % 10 == 0):
                #  print(i)
            #  print(".", end="")
            sys.stdout.flush()
            if not (fi.endswith(".html") or fi.endswith(".htm")):
                continue
            fn = root+"/"+fi
            fid = get_id(fn)
            with open(str(fid)+".txt", "w") as fout:
                try:
                    with open(fn, "r") as fin:
                        fr = fin.read()
                        soup = BeautifulSoup(fr)
                        print(str(fid), file=fout)
                        print("http://" + fn[2:], file=fout)
                        out = []
                        links = links_from_html(fr)
                        for link in links:
                            fp = "./" + link[7:]
                            if fp in file2id:
                                out.append(str(file2id[fp]))
                        print(" ".join(out), file=fout)
                        if soup.title:
                            print(soup.title.string, file=fout)
                        else:
                            print(file=fout)
                        print(text_from_html(fr), file=fout)
                except UnicodeDecodeError:
                    with open(fn, "r", encoding="cp936") as fin:
                        fr = fin.read()
                        soup = BeautifulSoup(fr)
                        print(str(fid), file=fout)
                        print("http://" + fn[2:], file=fout)
                        out = []
                        links = links_from_html(fr)
                        for link in links:
                            fp = "./" + link[7:]
                            if fp in file2id:
                                out.append(str(file2id[fp]))
                        print(" ".join(out), file=fout)
                        if soup.title:
                            print(soup.title.string, file=fout)
                        else:
                            print(file=fout)
                        print(text_from_html(fr), file=fout)
                except:
                    pass

if __name__ == "__main__":
    build_fileid()
    parse_files()

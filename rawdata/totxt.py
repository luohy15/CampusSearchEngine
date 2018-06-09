import sys
import os
from bs4 import BeautifulSoup
from visible import *
from getlinks import *

data_path = "/Users/rv/src/project/search_engine/rawdata"
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
    for root, dirs, files in os.walk(data_path): 
        for fi in files:
            if not (fi.endswith(".html") or fi.endswith(".htm")):
                continue
            print(",", end="")
            sys.stdout.flush()
            get_id(root+"/"+fi)

def parse_files():
    i = 0
    for root, dirs, files in os.walk(data_path): 
        for fi in files:
            print(".", end="")
            sys.stdout.flush()
            if not (fi.endswith(".html") or fi.endswith(".htm")):
                continue
            fn = root+"/"+fi
            fid = get_id(fn)
            with open("../DataParse/build/" + str(fid)+".txt", "w") as fout:
                try:
                    with open(fn, "r") as fin:
                        fr = fin.read()
                        soup = BeautifulSoup(fr)
                        print(str(fid), file=fout)
                        url = "http://" + fn[len(data_path)+1:];
                        print(url, file=fout)
                        out = []
                        links = links_from_html(fr, url)
                        for link in links:
                            fp = data_path + link[6:]
                            if fp in file2id:
                                out.append(str(file2id[fp]))
                        out = list(set(out))
                        print(" ".join(out), file=fout)
                        if soup.title:
                            if soup.title.string:
                                print(soup.title.string.replace("\n", ""), file=fout)
                            else:
                                print("", file=fout)
                        else:
                            print("", file=fout)
                        print(text_from_html(fr, fid), file=fout)
                except UnicodeDecodeError:
                    with open(fn, "r", encoding="cp936") as fin:
                        fr = fin.read()
                        soup = BeautifulSoup(fr)
                        print(str(fid), file=fout)
                        url = "http://" + fn[len(data_path)+1:];
                        print(url, file=fout)
                        out = []
                        links = links_from_html(fr, url)
                        for link in links:
                            fp = data_path + link[6:]
                            if fp in file2id:
                                out.append(str(file2id[fp]))
                        out = list(set(out))
                        print(" ".join(out), file=fout)
                        if soup.title:
                            if soup.title.string:
                                print(soup.title.string.replace("\n", ""), file=fout)
                            else:
                                print("", file=fout)
                        else:
                            print("", file=fout)
                        print(text_from_html(fr, fid), file=fout)
                except:
                    pass

def check_files():
    for i in range(len(file2id)):
        #  print(i+1)
        #  os.system("wc -l " + str(i + 1) + ".txt")
        count = len(open("../DataParse/build/" + str(i+1)+".txt").readlines())
        if count != 5:
            print(i + 1, count)


if __name__ == "__main__":
    build_fileid()
    parse_files()
    check_files()

import sys
import os
from bs4 import BeautifulSoup
from visible import *
from getlinks import *

data_path = "/home/fuck/allraw"
file2id = {}

assert(data_path[-1] != '/') # human makes mistakes

def get_id(s):
    if s in file2id:
        return file2id[s]
    else:
        file2id[s] = len(file2id) + 1
    return file2id[s]

def remove_id(i):
    print("remove %d" % i)
    assert(i == len(file2id))
    for f in file2id:
        if file2id[f] == i:
            file2id.pop(f)
            return

def build_fileid():
    for root, dirs, files in os.walk(data_path): 
        for fi in files:
            if not (fi.endswith(".html") or fi.endswith(".htm")):
                continue
            print(",", end="")
            sys.stdout.flush()
            fn = root+"/"+fi
            get_id(fn)
            fid = get_id(fn)
            try: # try to load with UTF8
                with open(fn, "r") as fin:
                    fr = fin.read()
                    soup = BeautifulSoup(fr)
            except UnicodeDecodeError:
                try: # then try to load with cp936
                    with open(fn, "r", encoding="cp936") as fin:
                        fr = fin.read()
                        soup = BeautifulSoup(fr)
                except: # damn file encoding, ignore
                    remove_id(fid)
                    soup = None
                    fid = -1
    for i in file2id:
        print(i, file2id[i])

def parse_files():
    for root, dirs, files in os.walk(data_path): 
        for fi in files:
            print(".", end="")
            sys.stdout.flush()
            if not (fi.endswith(".html") or fi.endswith(".htm")):
                continue
            fn = root+"/"+fi
            if fn in file2id:
                fid = file2id[fn]
            else:
                continue # this file is ignored
            with open("../DataParser/build/" + str(fid)+".txt", "w") as fout:
                print(str(fid), file=fout)
                url = "http://" + fn[len(data_path)+1:]
                print(url, file=fout)
                out = []
                try: # try to load with UTF8
                    with open(fn, "r") as fin:
                        fr = fin.read()
                        soup = BeautifulSoup(fr)
                except UnicodeDecodeError:
                    try: # then try to load with cp936
                        with open(fn, "r", encoding="cp936") as fin:
                            fr = fin.read()
                            soup = BeautifulSoup(fr)
                    except: # damn file encoding, ignore
                        assert(False)
                links = links_from_html(soup, url)
                for link in links:
                    fp = data_path + link[6:] # stupid hack
                    if fp in file2id:
                        out.append(str(file2id[fp]))
                out = list(set(out)) # stupid deduplicate
                print(" ".join(out), file=fout)
                if soup.title and soup.title.string:
                    print(soup.title.string.strip(), file=fout)
                else:
                    print("", file=fout)
                print(text_from_html(soup, fid), file=fout)


def check_files():
    for i in range(len(file2id)):
        #  print(i+1)
        #  os.system("wc -l " + str(i + 1) + ".txt")
        count = len(open("../DataParser/build/" + str(i+1)+".txt").readlines())
        if count != 5:
            print(i + 1, count)


if __name__ == "__main__":
    build_fileid()
    parse_files()
    check_files()

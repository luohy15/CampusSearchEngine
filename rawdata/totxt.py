import hashlib
from hashlib import sha1
import sys
import os
from bs4 import BeautifulSoup
from visible import *
from getlinks import *
#  sha1 = hashlib.sha1()
# BUF_SIZE is totally arbitrary, change for your app!
#  BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

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

def gettitle(s):
    soup = BeautifulSoup(open(s))
    return soup.title

def getcontent(s):
    pass

def work():
    fout = open("run.tmp", "w")
    with open("crawl.log", "r") as fin:
        lines = fin.readlines()
        for line in lines:
            tokens = line.strip().split()
            #  print(tokens, file=fout)
            dst = tokens[3]
            src = tokens[5]
            protocal = dst.split(":")[0]
            if protocal == "http":
                dstpath = dst.replace("http:/", os.getcwd())
                srcpath = src.replace("http:/", os.getcwd())
                if os.path.isfile(dstpath) and os.path.isfile(srcpath):
                    #  filesha1 = make_sha1(filepath)
                    print(dstpath+" "+srcpath, file=fout)
                    out[get_id(srcpath)].append(get_id(dstpath))
                    #  with open(filepath, 'rb') as f:
                        #  while True:
                            #  data = f.read(BUF_SIZE)
                            #  if not data:
                                #  break
                            #  sha1.update(data)
                    #  print("filesha:{0}".format(sha1.hexdigest())+"sha1digest:{0}".format(tokens[9]), file=fout)
        print(str(out), file=fout)
        for line in lines:
            tokens = line.strip().split()
            dst = tokens[3]
            protocal = dst.split(":")[0]
            if protocal == "http":
                dstpath = dst.replace("http:/", os.getcwd())
                if os.path.isfile(dstpath):
                    document_id = get_id(dstpath)
                    with open(str(document_id)+".txt", "w", encoding="utf8") as txtout:
                        print(str(document_id), file=txtout)
                        print(dst, file=txtout)
                        print(out[document_id], file=txtout)
                        print(gettitle(dstpath), file=txtout)
                        print(getcontent(dstpath), file=txtout)
    fout.close()

if __name__ == "__main__":
    build_fileid()
    parse_files()

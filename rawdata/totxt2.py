import os
import sys
import shlex
import subprocess 

data_path = "/home/fuck/allraw"
pdf_parser = "./pdf2txt"
doc_parser = "antiword"
docx_parser = "./docx2txt"
doc_output_path= "../DataParser/build"
docx_output_path= "../DataParser/build"
pdf_output_path= "../DataParser/build"

assert(data_path[-1] != '/')
assert(doc_output_path[-1] != '/')

n_doc = 0
n_docx = 0
n_pdf = 0

def pdf_output_fn(n):
    return pdf_output_path + ("/pdf%d.txt"%n)

def handlepdf():
    global n_pdf
    for root, dirs, files in os.walk(data_path):
        for fi in files:
            if not (fi.endswith(".pdf")):
                continue
            n_pdf += 1
            fn = root+"/"+fi
            url = "http://" + fn[len(data_path)+1:]
            try:
                output = subprocess.check_output([pdf_parser, fn])
            except:
                print("failed")
                n_pdf -= 1
                continue
            output = output.decode("utf8")
            output = " ".join(output.split()).strip()
            if (len(output) < 1):
                n_pdf -= 1
                continue
            print("%d ok" % n_pdf)
            with open(pdf_output_fn(n_pdf), "w") as fout:
                print(url.strip(), file=fout)
                print(output.strip(), file=fout)

def doc_output_fn(n):
    return doc_output_path + ("/doc%d.txt"%n)

def handledoc():
    global n_doc
    for root, dirs, files in os.walk(data_path):
        for fi in files:
            if not (fi.endswith(".doc")):
                continue
            n_doc += 1
            fn = root+"/"+fi
            url = "http://" + fn[len(data_path)+1:]
            try:
                output = subprocess.check_output([doc_parser, fn])
            except:
                n_doc -= 1
                print("failed")
                continue
            print("%d ok" % n_doc)
            try:
                output = output.decode("utf8")
            except UnicodeDecodeError:
                try:
                    output = output.decode("cp936")
                except:
                    n_doc -= 1
                    print("failed")
                    continue
            except:
                n_doc -= 1
                print("failed")
                continue
            output = " ".join(output.split())
            with open(doc_output_fn(n_doc), "w") as fout:
                print(url.strip(), file=fout)
                print(output.strip(), file=fout)

def docx_output_fn(n):
    return docx_output_path + ("/docx%d.txt"%n)

def handledocx():
    global n_docx
    for root, dirs, files in os.walk(data_path):
        for fi in files:
            if not (fi.endswith(".docx")):
                continue
            n_docx += 1
            fn = root+"/"+fi
            url = "http://" + fn[len(data_path)+1:]
            try:
                output = subprocess.check_output([docx_parser, fn])
            except:
                n_docx -= 1
                print("failed")
                continue
            print("%d ok" % n_docx)
            try:
                output = output.decode("utf8")
            except UnicodeDecodeError:
                try:
                    output = output.decode("cp936")
                except:
                    n_docx -= 1
                    print("failed")
                    continue
            except:
                n_docx -= 1
                print("failed")
                continue
            output = " ".join(output.split())
            with open(docx_output_fn(n_docx), "w") as fout:
                print(url.strip(), file=fout)
                print(output.strip(), file=fout)

if __name__ == "__main__":
    handledocx()

MAXX = 1000

txt_path = "."
fout = open("../../input/file.xml", "w", encoding="utf8")
escape = lambda s : s.replace("\"", "&quot;").replace("&", "&amp;")
print("<?xml version=\"1.0\" ?>\n<pics>\n<category name=\"sogou\">", file=fout)

get_title = lambda url: url[url.rindex('/')+1:]

for ft in ["pdf", "doc", "docx"]:
    i = 1
    while True:
        try:
            with open(txt_path + '/' + "%s%d.txt"%(ft,i), "r", encoding="utf8") as fin:
                lines = fin.readlines()
                if (len(lines) != 2):
                    print("Files should contain 2 lines")
                    break
                print("<pic title=\"%s\" fn=\"%s\" url=\"%s\"/>" % (
                    escape(get_title(lines[0].strip())),
                    "%s%d"%(ft,i),
                    escape(lines[0].strip())),
                    file=fout)
            i += 1
            if (i > MAXX):
                break
        except:
            print("Totally %d %s files found" % ((i-1), ft))
            break

print("</category>\n</pics>\n", file=fout)
fout.close()

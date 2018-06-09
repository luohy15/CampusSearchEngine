MAX_TXT = 120000
txt_path = "."
fout = open("../../input/html.xml", "w", encoding="utf8")
escape = lambda s : s.replace("\"", "'").replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")
print("<?xml version=\"1.0\" ?>\n<pics>\n<category name=\"sogou\">", file=fout)
i = 1
while True:
    try:
        with open(txt_path + '/' + "%s.txt"%i, "r", encoding="utf8") as fin:
            lines = fin.readlines()
            if (len(lines) != 6):
                print("Files should contain 6 lines")
                break
            print("<pic title=\"%s\" id=\"%s\" pr=\"%s\" url=\"%s\"/>" % (
                escape(lines[3].strip()), lines[0].strip(),
                lines[5].strip(), escape(lines[1].strip())), file=fout)
        i += 1
        if (i > MAX_TXT):
            break
        if (i % 1000 == 0):
            print(">>%d"%i)
    except:
        print("Totally %d files found" % (i-1))
        break
print("</category>\n</pics>\n", file=fout)
fout.close()

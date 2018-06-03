
n_txt = 3

fout = open("html.xml", "w", encoding="utf8")
print("<?xml version=\"1.0\" ?>\n<pics>\n<category name=\"sogou\">", file=fout)
for i in range(1, n_txt+1):
    with open("%s.txt"%i, "r", encoding="utf8") as fin:
        lines = fin.readlines()
        assert(len(lines) == 6)
        print("<pic title=\"%s\" id=\"%s\" pr=\"%s\" url=\"%s\"/>" % (
            lines[3].strip(), lines[0].strip(),
            lines[5].strip(), lines[1].strip()), file=fout)
print("</category>\n</pics>\n", file=fout)
fout.close()

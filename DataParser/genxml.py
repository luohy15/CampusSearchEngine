MAX_TXT = 500
fout = open("html.xml", "w", encoding="utf8")
print("<?xml version=\"1.0\" ?>\n<pics>\n<category name=\"sogou\">", file=fout)
i = 1
while True:
    try:
        with open("%s.txt"%i, "r", encoding="utf8") as fin:
            lines = fin.readlines()
            if (len(lines) != 6):
                print("Files should contain 6 lines")
                break
            print("<pic title=\"%s\" id=\"%s\" pr=\"%s\" url=\"%s\"/>" % (
                lines[3].strip(), lines[0].strip(),
                lines[5].strip(), lines[1].strip()), file=fout)
        i += 1
        if (i > MAX_TXT):
            break
    except:
        print("Totally %d files found" % (i-1))
        break
print("</category>\n</pics>\n", file=fout)
fout.close()

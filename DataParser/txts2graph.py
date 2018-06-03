fout = open("html.graph", "w", encoding="utf8")
i = 1
while True:
    try:
        with open("%s.txt"%i, "r", encoding="utf8") as fin:
            lines = fin.readlines()
            if (len(lines) != 5):
                print("Files should have 5 lines")
                break
            print("%s: %s"  % (lines[0].strip(), lines[2].strip()), file=fout)
        i += 1
    except:
        print("Totally %d files found" % (i-1))
        break
fout.close()


MAX_TXT = 120000
txt_path = "."
fout = open("html.graph", "w", encoding="utf8")
i = 1
while True:
    try:
        print("Reading %d" % i)
        with open(txt_path + '/' + "%s.txt"%i, "r", encoding="utf8") as fin:
            print("Reading %d" % i)
            lines = fin.readlines()
            if (len(lines) != 5):
                print("Files%d should have 5 lines"%i)
                break
            print("%s:"  % (lines[0].strip()), file=fout, end=" ")
            ll = [int(j) for j in lines[2].strip().split()]
            for j in ll:
                if j > 0 and j < MAX_TXT:
                    print("%d " % (j), file=fout, end="")
            print("", file=fout)
        i += 1
        if i > MAX_TXT: 
            break
        if i % 1000 == 0:
            print(">>%d"%i)
    except:
        print("Totally %d files found" % (i-1))
        break
fout.close()


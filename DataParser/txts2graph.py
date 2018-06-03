
n_txt = 3

fout = open("html.graph", "w", encoding="utf8")
for i in range(1, n_txt+1):
    with open("%s.txt"%i, "r", encoding="utf8") as fin:
        lines = fin.readlines()
        assert(len(lines) == 5)
        print("%s: %s"  % (lines[0].strip(), lines[2].strip()), file=fout)
fout.close()


import sys
out = open(sys.argv[2], 'w')
for line in open(sys.argv[1]):
    spl = line.strip().split()
    if len(spl) > 1:
        word, pos = spl[0], spl[1]
        out.write("{}_{} ".format(word, pos))
    else:
        out.write("\n")

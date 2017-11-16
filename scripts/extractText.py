import sys

infile=sys.argv[1]
outfile=sys.argv[2]

f=open(infile)

o=open(outfile, 'w')

ws=f.readlines()

for w in ws:
    if w == "" or w.isspace():
        o.write('\n')
    else:
        o.write("{}\t_\n".format(w.split('_')[0]))

o.close()
f.close()



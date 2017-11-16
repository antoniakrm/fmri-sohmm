import sys 

lines=[l.strip().split() for l in open(sys.argv[1]).readlines()]
glines=[l.strip().split() for l in open(sys.argv[2]).readlines()]

for i in range(len(lines)):
    if len(lines[i])<2: 
        print ""
    elif glines[i][0][0] not in ["@","#"] and glines[i][0][:4]!="http" and len(glines[i][0])>1:
        lines[i]=[lines[i][0],'I-'+glines[i][-1],'I-'+lines[i][-1]]
        print " ".join(lines[i])
   

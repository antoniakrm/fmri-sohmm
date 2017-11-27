iter=30
split=te

#Input either token or baseline

if [ "$1" = "token" ]
then
echo "Token"
VECS="vecs/potter-8-4.0-10.0-10-tokens.vecs"
SYSTEM="token"
fi

if [ "$1" = "baseline" ]
then
echo "Baseline"
VECS=""
SYSTEM="bl"
fi

# generate embedfeatures.txt
echo 'WordIdLower 10' > $SYSTEM.embedfeatures.txt;
echo 'PatternMatchPipe .*-.* hyphen' >> $SYSTEM.embedfeatures.txt;
echo 'PatternMatchPipe \p{javaUpperCase}.* capital' >> $SYSTEM.embedfeatures.txt;
echo 'PatternMatchPipe .*[0-9].* digit' >> $SYSTEM.embedfeatures.txt;
echo "PatternMatchPipe [.,!?:;()\"/\[\]'«-]+ punct"  >> $SYSTEM.embedfeatures.txt;
echo 'SuffixPipe 1 20'  >> $SYSTEM.embedfeatures.txt;
echo 'SuffixPipe 2 20' >> $SYSTEM.embedfeatures.txt;
echo 'SuffixPipe 3 20' >> $SYSTEM.embedfeatures.txt;
if [ "$SYSTEM" != "bl" ] 
then
echo 'WordEmbeddingsPipe '$VECS >> $SYSTEM.embedfeatures.txt 
fi

# generate potter.params
echo 'name=English' > potter.params;
echo 'lowercase=false' >> potter.params;
echo 'transductive=false' >> potter.params;
echo 'unknown-words-thresh=0' >> potter.params;
echo 'reader-type=acl2011' >> potter.params;
echo 'train-name=TRAIN' >> potter.params;
echo 'train-file=data/potter.tr.conll' >> potter.params;
echo 'dev-name=DEV' >> potter.params;
echo 'dev-file=data/potter.dv.conll' >> potter.params;
echo 'test-name1=TEST1' >> potter.params;
echo 'test-file1=data/potter.te.conll' >> potter.params;

java -Xmx32g -jar lib/sohmm.jar train potter.params en-wik-20120320.params $SYSTEM.embedfeatures.txt output/ $iter acc;

java -Xmx32g -jar lib/sohmm.jar tag data/potter.$split.conll $SYSTEM.embedfeatures.txt output/ data/potter.$split.$SYSTEM.out acc;

python scripts/conll2BIO.py data/potter.$split.$SYSTEM.out data/potter.$split.conll > data/potter.$split.$SYSTEM.out.bio;
perl scripts/conlleval.pl < data/potter.$split.$SYSTEM.out.bio;

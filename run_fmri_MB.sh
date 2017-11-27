iter=30
split=te

#Input either token, type or baseline

if [ "$1" = "type" ]
then
echo "Type"
#VECS="vecs/potter-4-0.0-8.0-10_types.vecs"
#VECS="vecs/potter-8-4.0-10.0-10-type_normal.vecs"
#VECS="vecs/potter-8-4.0-10.0-10-type_lower.vecs"
#VECS="vecs/typegrouped_lowercase.csv"
VECS="vecs/typegrouped_normalcase.csv"
#VECS="/Users/Maria/Documents/CST/THC/glove.6B.300d.txt"
SYSTEM="type"
fi

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
#echo 'train-file=data/potter.tr.conll' >> potter.params;
echo 'train-file=data/potter.tr.no_id.conll' >> potter.params;
echo 'dev-name=DEV' >> potter.params;
#echo 'dev-file=data/potter.dv.conll' >> potter.params;
echo 'dev-file=data/potter.dv.no_id.conll' >> potter.params;
echo 'test-name1=TEST1' >> potter.params;
#echo 'test-file1=data/potter.te.conll' >> potter.params;
echo 'test-file1=data/potter.te.no_id.conll' >> potter.params;

java -Xmx32g -jar lib/sohmm.jar train potter.params en-wik-20120320.params $SYSTEM.embedfeatures.txt output/ $iter acc;

java -Xmx32g -jar lib/sohmm.jar tag data/potter.$split.no_id.conll $SYSTEM.embedfeatures.txt output/ data/potter.$split.$SYSTEM.out acc;

python scripts/conll2BIO.py data/potter.$split.$SYSTEM.out data/potter.$split.no_id.conll > data/potter.$split.$SYSTEM.out.bio;
#python scripts/conll2BIO.py data/potter.$split.$SYSTEM.out data/potter.$split.conll > data/potter.$split.$SYSTEM.out.bio;
perl scripts/conlleval.pl < data/potter.$split.$SYSTEM.out.bio;

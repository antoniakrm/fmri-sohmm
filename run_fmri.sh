iter=30
split=te



subjects=$1
lookback=$2
lookout=$3
dimensions=$4

vecfile=potter-$subjects-$lookback-$lookout-$dimensions.vecs
# generate embedfeatures.txt
echo 'WordIdLower 10' > embedfeatures.txt
echo 'PatternMatchPipe .*-.* hyphen' >> embedfeatures.txt
echo 'PatternMatchPipe \p{javaUpperCase}.* capital' >> embedfeatures.txt
echo 'PatternMatchPipe .*[0-9].* digit' >> embedfeatures.txt
echo "PatternMatchPipe [.,!?:;()\"/\[\]'«-]+ punct"  >> embedfeatures.txt
echo 'SuffixPipe 1 20'  >> embedfeatures.txt
echo 'SuffixPipe 2 20' >> embedfeatures.txt
echo 'SuffixPipe 3 20' >> embedfeatures.txt
echo 'WordEmbeddingsPipe data/vecs/'$vecfile >> embedfeatures.txt

# generate potter.params
echo 'name=English' > potter.params
echo 'lowercase=false' >> potter.params
echo 'transductive=false' >> potter.params
echo 'unknown-words-thresh=0' >> potter.params
echo 'reader-type=acl2011' >> potter.params
echo 'train-name=TRAIN' >> potter.params
echo 'train-file=data/potter.tr.conll' >> potter.params
echo 'dev-name=DEV' >> potter.params
echo 'dev-file=data/potter.dv.conll' >> potter.params
echo 'test-name1=TEST1' >> potter.params
echo 'test-file1=data/potter.te.conll' >> potter.params

python src/convert_data.py -d fmri/data -s $subjects --dim $dimensions --lookback $lookback --lookout $lookout -o potter
#mv $vecfile data

java -Xmx32g -jar lib/sohmm.jar train potter.params en-wik-20120320.params embedfeatures.txt output/ $iter acc

java -Xmx32g -jar lib/sohmm.jar tag data/potter.$split.conll embedfeatures.txt output/ data/potter.$split.out acc

python scripts/conll2BIO.py data/potter.$split.out data/potter.$split.conll > data/potter.$split.out.bio
perl scripts/conlleval.pl < data/potter.$split.out.bio

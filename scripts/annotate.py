# -*- coding: utf-8 -*-
"""
annotate a tweet in CoNLL format with universal tags

USAGE:
\tpython annotate.py <folder>

Created on Mon Aug 26 14:05:53 2013

@author: dirkhovy
"""

import sys, readline, glob, os
TAGS = set(["VERB","NOUN","PRON","ADJ","ADV","ADP","CONJ","DET","NUM","PRT","X",".",    'FLAG'])

# frequent word class examples
AUX_VERBS = set(["is", "are", "have", "was", "be", "get", "can", "do", "will", "got", "love", "go", "don't", "know", "need", "see", "going", "would", "think", "has", "please", "should", "can't", "want", "gonna", "say", "like", "follow", "come", "let", "had", "check", "said", "did", "am", "wait", "try", "take", "make", "hate", "been", "took", "start", "read", "hear", "getting", "could", "told", "looks", "live", "gotta", "does", "win", "wanna", "thought", "thank", "seen", "r", "made", "looking", "keep", "having", "find", "feel", "came", "ask", "were", "watch", "put", "meet", "may", "leave", "happened", "give", "dont", "doesn't", "being", "won't", "welcome", "wanted", "trying", "tell", "talk", "singing", "rt", "posted", "might", "hope", "help", "enjoy", "eat", "doing", "didn't", "coming", "bring", "wish", "watched", "waiting", "vote", "used", "i'm", "you're", "he's", "she's", "it's", "we're", "they're"])
PRONOUNS = set(['i', 'me', 'you', 'he', "him", 'she', 'her', 'we', 'us', "they", "them", 'myself', 'youself', 'himself', 'herself', 'ourselves', 'yourselves', 'themselves', 'it', 'itself'])
PREPS = set(["'cept", "'fore", "'gainst", "'mongst", "abaft", "aboard", "about", "above", "across", "afore", "after", "against", "along", "alongside", "amid", "amidst", "among", "amongst", "apropos", "around", "as", "astride", "at", "atop", "bar", "barring", "before", "behind", "below", "beneath", "beside", "besides", "between", "betwixt", "beyond", "but", "by", "chez", "concerning", "considering", "despite", "down", "during", "ere", "ex", "except", "excepting", "excluding", "following", "for", "from", "in", "including", "inside", "into", "less", "like", "minus", "near", "neath", "nigh", "notwithstanding", "o'", "o'er", "of", "off", "on", "onto", "opposite", "outside", "outwith", "over", "pace", "past", "pending", "per", "plus", "pro", "re", "regarding", "respecting", "round", "save", "since", "than", "thro'", "through", "throughout", "thru", "till", "to", "toward", "towards", "under", "underneath", "unlike", "until", "unto", "up", "upon", "versus", "via", "with", "within", "without"])
SMILEYS = set(["rt", "...", ":)", "—", "smh", "<3", ";)", "-", "|", ")", ":(", "<", "cont", "(", "-_-", "#nowplaying", ":d", "y", "xd", "«", ":/", ">", "#whodoesthat", "t", "", "(:", ";", "-->", "<<", "#tcot", "s", "o_o", "#glee", "e", "£", ":))", "--", "->", ">>", "<--"])
PUNCS = set(['.', ',', '?', '!', "'", '"', ':', ';', '...'])
CONJUNCTIONS = set(["&", "+", "and", "but", "n", "'n", "nd", "'nd", "or"])
DETS = set(["a", "all", "alll", "an", "another", "any", "both", "d", "da", "dat", "dis", "every", "her", "his", "is", "its", "ma", "mah", "my", "myyyyyyyyyy", "no", "our", "some", "tha", "that", "the", "their", "them", "themm", "there", "these", "they", "this", "those", "tht", "u", "ur", "what", "which", "ya", "y'all", "your"])
NOUNS = set(["day", "people", "time", "thanks", "video", "shit", "home", "tumblr", "game", "number", "man", "girl", "thing", "show", "morning", "lebron", "work", "way", "tomorrow", "heat", "love", "year", "school", "nigga", "news", "life", "everything", "world", "things", "something", "someone", "photo", "night", "face", "baby", "twitter", "team", "south", "party", "part", "miami", "halloween", "facebook", "everyone", "dude", "wednesday", "times", "sis", "reason", "pic", "mind", "lakers", "james", "hell", "hair", "guys", "friend", "bro", "bitch", "ass", "week", "tonight", "stuff", "state", "song", "smith", "self", "season", "practice", "phone", "park", "page", "october", "music", "movie", "mom", "lunch", "link", "la", "lady", "house", "hand", "god", "fans", "dollar", "dick", "days", "computer", "code", "class", "city", "chick", "celtics", "business", "blow", "birthday", "youtube", "yahoo", "women", "follower", "followers"])
ADJS = set(["new", "good", "more", "last", "great", "bad", "only", "many", "number", "lil", "happy", "best", "old", "next", "little", "better", "sad", "real", "nice", "much", "hot", "free", "first", "different", "cute", "sure", "same", "right", "ready", "nasty", "late", "big", "ugly", "such", "sick", "sexy", "hilarious", "funny", "fine", "favorite", "early", "damn", "cool", "awesome", "young", "worst", "whole", "white", "true", "sweet", "sorry", "social", "serious", "refreshing", "online", "lost", "long", "live", "high", "hard", "fun", "fresh", "fav", "dumb", "close", "black", "beautiful", "younger", "wrong", "worse", "weird", "weekly", "up", "stupid", "smart", "silly", "sexual", "senior", "scary", "sappy", "ridiculous", "republican", "red", "random", "quick", "public", "pregnant", "possible", "personal", "other", "orange", "open", "lazy", "innovative", "important", "hungry", "huge", "green", "glad", "gay"])
ADVS = set(["just", "now", "how", "not", "so", "why", "when", "too", "really", "where", "never", "here", "still", "ever", "always", "more", "there", "then", "even", "back", "right", "as", "again", "down", "actually", "well", "tonight", "tho", "pretty", "better", "away", "together", "much", "like", "far", "also", "all", "yet", "y", "wen", "that", "sooo", "soon", "seriously", "probably", "over", "often", "no", "most"])


def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return raw_input(prompt)
   finally:
      readline.set_startup_hook()


# iterate over all files
#for i, in_file in enumerate(sorted(glob.iglob("%s/*.txt" % sys.argv[1]) )):
for i, in_file in enumerate([sys.argv[1]]):

    out_file = "%s.tagged" % in_file
    # check whether annotated file exists already
    if os.path.isfile(out_file):
        sys.stderr.write('annotations for %s already exist, skipping file... (delete %s to re-annotate file)\n' % (in_file, out_file))
        continue

    sys.stderr.write("\x1b[2J\x1b[H")

    words = map(str.strip, open(in_file, 'rU').readlines())
    tags = []
    
    print '%s. %s' % (i+1, in_file)
    print
    print "SENTENCE:\t%s" % (' '.join(words))
    print "TAGS:\t\t%s" % (', '.join(TAGS))
    print '-----------------------------------------------------------------------------------'
    print "use arrows to go through previously used tags. Type 'quit' to exit, 'b' to go back a word."
    print "use extra tag 'FLAG' to mark unclear words for later inspection"
    print "Frequent words might come with tag suggestions"
    print
    
    w = 0
    while w < len(words):
        word = words[w]
        tag = None
        go_back = False
        
        while tag == None or tag.upper() not in TAGS:
            
            # check whether word is in some form of closed class to make suggestions
            default = ""
            if word in PUNCS:
                default = '.'
            elif word == "NUMBER":
               default = "NUM"
            elif word in ['@USER', "URL"] or word.lower() in NOUNS:
                default = 'NOUN'
            elif word.lower() in AUX_VERBS:
                default = 'VERB'
            elif word.lower() in PRONOUNS:
                default = 'PRON'
            elif word.startswith(':-') or word in SMILEYS:
                default = 'X'
            elif word.lower() in PREPS:
                default = 'ADP'
            elif word.lower() in DETS:
                default = 'DET'
            elif word.lower() in CONJUNCTIONS:
                default = 'CONJ'
            elif word.lower() in ADJS:
                default = 'ADJ'
            elif word.lower() in ADVS:
                default = 'ADV'
                
            # get the input
            tag = rlinput("%s. %s: " % (w+1, word), prefill=default)

            if tag == 'quit':
                sys.exit()
            elif tag == 'b':
                go_back = True
                break
            
        if go_back:
            del tags[-1]
            w -= 1
            continue
        else:
            tags.append(tag.upper())
            w += 1

    assert len(words) == len(tags), "number of tags does not match words!"
    
    out = open(out_file, 'w')
    for word, tag in zip(words, tags):
        out.write("%s\t%s\n" % (word, tag))
    out.close()

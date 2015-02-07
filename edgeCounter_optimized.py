import csv
import re
import random
from time import time
from pymongo import MongoClient
from nltk.corpus import stopwords
from nltk.corpus import brown
from nltk.stem.snowball import EnglishStemmer
from nltk.tokenize import RegexpTokenizer


#Helper for processTweets
def preprocessTweet(tweetText):

	#Convert to unicode.
	#Must encode then re-encode because of some funky mixing of strings and unicode in tweets.
	start = time()
	pTweet = tweetText.encode('UTF-8', 'ignore').decode('UTF-8', 'ignore')
	encF = time()

	#Remove URLs
	pTweet = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', u'', pTweet);
	#Remove Non-ASCII Unicode
	pTweet = re.sub(r'[^\x00-\x7F]+',u'',pTweet).lower();
	finish = time()
	#print "Enconding time percentage: ", (((encF-start)/(finish-start))*100), "%"

	return pTweet

	#Remove Hashtags
	#pTweet = re.sub('#\w+', '', pTweet);

#Takes a list of tweet objects and returns a corpus set object
#and a list of tweet objects with URLs, Stopwords, and Emoji removed, and all words stemmed.
#spanish is a set of Spanish stopwords which do not occur in English.
def processTweet(tweetText, tokenizer, stemmer, stops, spanish):


	#All Spanish stopwords which do not also occur in english.
	corpus = list()

	start = time()
	#Remove URLs and Emoji, convert to lowercase, convert to unicode string.
	text = preprocessTweet(tweetText);
	ppF = time()

	wordList = [w for w in tokenizer.tokenize(text) if w not in stops]


	tweetIsSpanish = False
	for w in wordList:
		if w in spanish:
			tweetIsSpanish = True


	if tweetIsSpanish:
		#Skip the tweet.
		return (list(), list())

	else:
		#Loop optimization
		cApp = corpus.append
		stemF = stemmer.stem
		#Stem each word and add it to the corpus.
		for i, word in enumerate(wordList):
			stem = stemF(word)
			wordList[i] = stem
			cApp(stem)

	finish = time()
	#print "Preprocess time percentage: ", (((ppF-start)/(finish-start))*100), "%"
	return (wordList, corpus);




def cleanWord(word):
	cleaned = word.decode('UTF-8', 'ignore').encode('UTF-8', 'ignore').lower()
	cleaned = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', u'', cleaned);
	cleaned = re.sub(r'\W+', u'', cleaned)

	return re.sub(r'[^\x00-\x7F]+',u'', cleaned);


#Reducer
#Takes a list of pairs to count, and a dictionary to store the counts in.
#Returns a dictionary with the pairs as keys, and the occurences of the pair as values.
def countPairs(pairs, pairCounts):

	for pair in pairs:
		try:
			oldCount = pairCounts[pair]
			pairCounts[pair] = oldCount + 1

		#Check for the pair in reverse order.
		except KeyError:
			splitPair = pair.split('\t')
			reversePair = splitPair[1]+'\t'+splitPair[0]

			try:
				oldCount = pairCounts[reversePair];
				pairCounts[reversePair] = oldCount + 1;

			except KeyError:
				pairCounts[pair] = 1;

	return pairCounts;

#Mapper
#Returns a list of strings representing pairs.
#Strings are in the format: 'word1\tword2'
def getPairs(wordList):
	pairs = list()
	app = pairs.append

	#Get all the co-occurence pairs in the tweet.
	for i, wordOne in enumerate(wordList):
		for j in xrange(i+1, len(wordList)):
			wordTwo = wordList[j];

			if wordOne != wordTwo:
				pair  = wordOne+'\t'+wordTwo
				app(pair)

	return pairs;


def processParagraph(paragraph, stemmer, stopwordList):
	wordList = [];
	filterWords = stopwordList
	filterWords.append('')

	for sentence in paragraph:
		for word in sentence:

			cWord = cleanWord(word)

			#Stem each word and return the resulting list of words along with a corpus.
			if cWord not in filterWords:
				stem = stemmer.stem(cWord)
				wordList.append(stem);

	return(wordList, set(wordList))



#Writes the information to a csv file read for import to GraphLab.
#fileName is the desired fileName for the output.
#pairs is the dictionary with the pair information.
#threshold is the minimum edge weight for the edge to be recorded.
def writeCSV_graphlab(fileName, corpus, pairs, threshhold):

	vertexPath = "csv/"+fileName+"_vertices_GL.csv";
	edgePath = "csv/"+fileName+"_edges_GL.csv";

	vertId = dict();


	with open(vertexPath, 'w') as vertF:
		vertHeaders = ['id', 'word'];
		csvWriter = csv.writer(vertF)
		csvWriter.writerow(vertHeaders)

		for index, vert in enumerate(corpus):
			vertId[vert] = index;
			line = [index, vert.encode('UTF-8','xmlcharrefreplace')]
			csvWriter.writerow(line);


	with open(edgePath, 'w') as edgeF:
		edgeHeaders = ['Word 1', 'Word 2', 'Co-occurrence']
		csvWriter = csv.writer(edgeF)
		csvWriter.writerow(edgeHeaders)

		for pair, count in pairs.iteritems():
			if count > threshhold:
				wordOne, wordTwo = pair.split('\t');
				line = [vertId.get(wordOne), vertId.get(wordTwo), str(count)];
				csvWriter.writerow(line);


#Writes the information to a csv file.
#fileName is the desired fileName for the output.
#corpus is an iterable with all unique words in pairs.
#pairs is the dictionary with the pair information.
#threshold is the minimum edge weight for the edge to be recorded.
def writeCSV(fileName, corpus, pairs, threshhold):

	vertexPath = "csv/"+fileName+"_vertices.csv";
	edgePath = "csv/"+fileName+"_edges.csv";



	with open(vertexPath, 'w') as vertF:
		vertHeaders = ['Word'];
		csvWriter = csv.writer(vertF)
		csvWriter.writerow(vertHeaders)

		for vert in corpus:
			line = vert.encode('UTF-8','xmlcharrefreplace')
			csvWriter.writerow(line);


	with open(edgePath, 'w') as edgeF:
		edgeHeaders = ['Word 1', 'Word 2', 'Occurrences']
		csvWriter = csv.writer(edgeF)
		csvWriter.writerow(edgeHeaders)

		for pair, count in pairs.iteritems():
			if count > threshhold:
				wordOne, wordTwo = pair.encode('UTF-8','xmlcharrefreplace').split('\t');
				line = [wordOne, wordTwo, str(count)];
				csvWriter.writerow(line);

def getCSVType():
	useGL = raw_input('Desired CSV format? (Please enter a letter...)\nPlain(p), GraphLab(g), or Both(b): ')
	if useGL == 'p' or useGL == 'g' or useGL == 'b':
		return useGL
	else:
		return getCSVType()


def countCorpus(corp):

	stemmer = EnglishStemmer(True)
	stops = stopwords.words("english")

	#Our corpus for the words which appear in our set of pairs.
	pairCorpus = set()
	pairCounts = dict()
	print "Processing..."
	i = 0

	for para in corp.paras():

		#Process the raw paragraph.
		processed, tempCorpus = processParagraph(para, stemmer, stops)

		#Find the pairs of words in the paragraph.
		pairs = getPairs(processed)

		#Count the pairs.
		pairCounts = countPairs(pairs, pairCounts)

		#Add any new words to our pairCorpus
		pairCorpus = pairCorpus.add(tempCorpus)

		if i % 2000 == 0:
			print str(i)+" paragraphs completed."

		i += 1

	return (pairCounts, pairCorpus)


def countMongo(mongoIter):

	tokenizer = RegexpTokenizer(r'\w+')
	stemmer = EnglishStemmer(True)
	stops = frozenset(stopwords.words("english"))
	spanish = frozenset(stopwords.words("spanish")).difference(stops)

	#Our corpus for the words which appear in our set of pairs.
	pairCorpus = set()
	pairCounts = dict()

	print "Processing..."
	i = 0

	#Loop Optimization
	cUpdate = pairCorpus.update
	for tweet in mongoIter:

		text = tweet['text'];

		start = time()
		processS = time()
		#Process the raw paragraph.
		processed, tempCorpus = processTweet(text, tokenizer, stemmer, stops, spanish)
		processF = time()

		#Find the pairs of words in the paragraph.
		pairS = time()
		pairs = getPairs(processed)
		pairF = time()

		#Count the pairs.
		countS = time()
		pairCounts = countPairs(pairs, pairCounts)
		countF = time()

		finish = time()
		#Add any new words to our pairCorpus
		cUpdate(tempCorpus)

		if i % 2000 == 0 and i > 0:
			print str(i)+" Rows completed."
			tTime = finish - start
			#print "Processing Time: ", (((processF-processS)/tTime)*100), "%"
			#print "Pair Time: ", (((pairF-pairS)/tTime)*100), "%"
			#print "Count Time: ", (((countF-countS)/tTime)*100), "%"

			#if i == 1000000:
			#	break;
		i += 1

	return (pairCounts, pairCorpus)

def randomMongo(db):
        while True:
                sample_size = int(raw_input('Sample Size? (enter 0 for full dataset): '))
                if sample_size == 0:
                        tweetIter = db.find({},{"text":1})
                        return tweetIter
                elif sample_size > 0:
                        tweetIter = db.find({},{"text":1})
                        tweet_list = [x for x in tweetIter]
                        random_tweets = random.sample(tweet_list,sample_size)
                        return random_tweets

#Takes an array of tweet objects.
def main():


	dbclient = MongoClient('z')
	db = dbclient.new_boston
	mongo_config = db.tweets

	tweetIter = randomMongo(mongo_config)

	threshhold = int(raw_input('Minimum edge threshold: '))
	useGL = getCSVType()
	fName = raw_input('Destination file name: ')
	pairCounts, corpus = countMongo(tweetIter)

	print "Counting complete.\n"

	if useGL == 'p':
		writeCSV(fName, corpus, pairCounts, threshhold);
	elif useGL == 'g':
		writeCSV_graphlab(fName, corpus, pairCounts, threshhold);
	else:
		writeCSV(fName, corpus, pairCounts, threshhold);
		writeCSV_graphlab(fName, corpus, pairCounts, threshhold);

	print "Writing complete."
	exit()


main()

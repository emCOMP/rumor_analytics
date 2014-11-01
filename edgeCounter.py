import re
import csv
from pymongo import MongoClient
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import EnglishStemmer

#Reducer
#Takes a list of pairs.
#Returns a dictionary with the pairs as keys, and the occurences of the pair as values.
def countPairs(pairs):
	pairCounts = dict();

	for pair in pairs:
		if pair in pairCounts:
			oldCount = pairCounts.get(pair);
			pairCounts[pair] = oldCount + 1;

		#Check for the pair in reverse order.
		else:
			splitPair = pair.split('\t')
			reversePair = splitPair[1]+'\t'+splitPair[0]

			if reversePair in pairCounts:
				oldCount = pairCounts.get(reversePair);
				pairCounts[reversePair] = oldCount + 1;
			
			else:
				pairCounts[pair] = 1;

	return pairCounts;

#Mapper
#Returns a list of strings representing pairs.
#Strings are in the format: 'word1\tword2'
def getPairs(tweetList):

	pairs = list()
	#times = dict()

	for tweet in tweetList:
		tokens = tweet['tokens']
		#time  = tweet['time']
		#Get all the co-occurence pairs in the tweet.
		for i, wordOne in enumerate(tokens):
			for j in range(i+1, len(tokens)):
				wordTwo = tokens[j];
				pair  = wordOne+'\t'+wordTwo

				pairs.append(pair)

				#if pair in times:
				#	times[pair].add();

	return pairs;


#Helper for processTweets
def preprocessTweet(tweetText):
	
	#Convert to unicode. 
	#Must encode then re-encode because of some funky mixing of strings and unicode in tweets.
	pTweet = tweetText.encode('UTF-8', 'ignore').decode('UTF-8', 'ignore')

	#Remove URLs
	pTweet = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', pTweet);
	
	#Remove Non-ASCII Unicode
	return re.sub(r'[^\x00-\x7F]+',u'',pTweet);

	#Remove Hashtags
	#pTweet = re.sub('#\w+', '', pTweet);

#Takes a list of tweet objects and returns a corpus set object
#and a list of tweet objects with URLs, Stopwords, and Emoji removed, and all words stemmed.
def processTweets(tweetList):
	
	tokenizer = RegexpTokenizer(r'\w+')
	stemmer = EnglishStemmer(True)
	stops = set(stopwords.words("english"))

	newTweets = list()
	corpus = set()

	#Get the tweet text and tokenize it.
	for tweet in tweetList:
		#Remove URLs and Emoji, convert to lowercase, convert to unicode string.
		text = preprocessTweet(tweet['text']).lower();
		wordList = [w for w in tokenizer.tokenize(text) if w not in stops]

		#Stem each word and add it to the corpus.
		for i, word in enumerate(wordList):
			stem = stemmer.stem(word)
			wordList[i] = stem
			corpus.add(stem)

		#Construct a new tweet with the processed information.
		newTweet = {'tokens': wordList}
		newTweets.append(newTweet)

	return (newTweets, corpus);


#Writes the information to a csv file.
#fileName is the desired fileName for the output.
#pairs is the dictionary with the pair information.
#threshold is the minimum edge weight for the edge to be recorded.
def writeCSV(fileName, pairs, threshhold):

	writePath = "csv/"+fileName;
	with open(writePath, 'w') as f:
		headers = ['Word 1', 'Word 2', 'Occurrences']
		csvWriter = csv.writer(f)
		csvWriter.writerow(headers)

		for pair, count in pairs.iteritems():
			if count > threshhold:
				wordOne, wordTwo = pair.encode('UTF-8','xmlcharrefreplace').split('\t');
				line = [wordOne, wordTwo, str(count)];
				csvWriter.writerow(line);

#Takes an array of tweet objects.
def main():
	tweetLimit = int(raw_input('Number of tweets to process: '))
	threshhold = int(raw_input('Minimum edge threshold: '))
	tweetIter = mongo_config.find().limit(tweetLimit)
	fName = raw_input('Destination file name: ')
	print "Processing..."
	processed = processTweets(tweetIter)
	pTweets = processed[0]
	corpus = processed[1]
	print "Counting..."
	pairs = getPairs(pTweets)
	pairCounts = countPairs(pairs)
	print "Counting complete.\n"
	print "Corpus"
	print corpus
	print '\n'
	writeCSV(fName, pairCounts, threshhold)
	print "Writing complete."
	exit()





dbclient = MongoClient('z')
db = dbclient.new_boston
mongo_config = db.tweets

#testIter = mongo_config.find().limit(100)

'''
testTweets = [];
testTweets.append({'text': 'The quick brown fox is spry.', 'TIMESTAMP': "12:00"});
testTweets.append({'text': 'Check this out! http://en.wikipedia.org/wiki/Emotion_classification', 'TIMESTAMP': "12:00"});
testTweets.append({'text': 'Mr. Bates please report to the office on the second floor and pick up your brown fox. #pissed', 'TIMESTAMP': "1:00"});
testTweets.append({'text': 'Mr. Bates, we are still waiting for you to pick up your brown fox.', 'TIMESTAMP': "2:00"});
testTweets.append({'text': 'Mr. Bates please come quickly. We all want to go home.', 'TIMESTAMP': "3:00"});
testTweets.append({'text': 'If there is a Mr. Bates in the building please report to the office on the second floor.', 'TIMESTAMP': "4:00"});
'''

main()






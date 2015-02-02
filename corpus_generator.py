'''
graph_bulder.py
============================================================
Description:

Builds a word-co-occurence graph from a database of tweets.
Outputs three CSVs: 
	<name>_v.csv -Vertex List
	<name>_e.csv -Edge List
	<name>_e_wNames.csv -Edge List with the Word Names rather than id numbers.
	<name>_info.txt -Information about the set. (Number of items processed, etc.)

---------------------------------
Notes:

-Stems all words
-Removes stopwords.
-Ignores tweets containing Spanish stopwords.

---------------------------------
TODO:

-Add support for filtering other languages from tweets?
'''

import csv
import re
import random
from pymongo import MongoClient
from nltk.corpus import stopwords
from nltk.stem.snowball import EnglishStemmer
from nltk.tokenize import RegexpTokenizer

corpusSize = 0

#Helper for processTweets
def clean_tweet(tweetText):
	
	#Convert to unicode. 
	#Must encode then re-encode because of some funky mixing of strings and unicode in tweets.
	pTweet = tweetText.encode('UTF-8', 'ignore').decode('UTF-8', 'ignore')
	pTweet = re.sub(r'@\w+', u'', pTweet);


	#Remove URLs
	pTweet = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', u'', pTweet);
	
	#Remove Non-ASCII Unicode
	pTweet = re.sub(r'[^\x00-\x7F]+',u'',pTweet).lower();
	
	return pTweet

	#Remove Hashtags NOTE: We are currently treating hashtags as words.
	#pTweet = re.sub('#\w+', '', pTweet);


#Takes a list of tweet objects and returns a corpus set object
#and a list of tweet objects with URLs, Stopwords, and Emoji removed, and all words stemmed.
#'spanish' is a set of Spanish stopwords which do not occur in English.
def process_tweet(tweetText, tokenizer, stemmer, filterWords):

	#Remove URLs and Emoji, convert to lowercase, convert to unicode string.
	text = clean_tweet(tweetText);
	wordList = [w for w in tokenizer.tokenize(text)]

	toFilter = False
	
	#Detect Spanish Tweets, RTs.
	for w in wordList:
		if w in filterWords:
			toFilter = True
			

	if toFilter:
		#Skip the tweet.
		return (list(), list())

	else:
		#Increment the corpus size.
		global corpusSize
		corpusSize += 1

		#Function alias for optimization
		stemF = stemmer.stem

		#Stem each word.
		for i, word in enumerate(wordList):
			stem = stemF(word)
			wordList[i] = stem

	return wordList;


#Builds the graph out of a mongoDB iterator.
#outPath is the path to output the corpus.
def corpus_from_mongo(mongoIter, outPath):

	tokenizer = RegexpTokenizer(r'\w+')
	stemmer = EnglishStemmer(True)

	###########
	filterWords = set(stopwords.words())
	filterWords.difference_update(set(stopwords.words('english')))
	filterWords.add('rt')
	filterWords = frozenset(filterWords)

	print "Processing..."
	
	#Loop counter for printing progress messages.
	i = 0

	#Count the number of non-junk tweets.
	global corpusSize
	corpusSize = 0

	with open(outPath, 'wb') as out:
		for tweet in mongoIter:
			
			text = tweet['text'];

			#Process the raw paragraph.
			processed = process_tweet(text, tokenizer, stemmer, filterWords)

			#If the tweet did not get thrown out.
			try:
				if processed[0]:
					#Count it toward the corpus size
					corpusSize += 1

					#Write the proccessed tweet to the file.
					t = ' '.join(processed)
					t += '\n'
					out.write(t)
			except:
				continue

			#Print Progress Updates
			if i % 2000 == 0 and i > 0:
				print str(i)+" Rows completed."

			i += 1
	
		
	print "\nProcessing complete.\n"
	print "Net tweets processed: ", corpusSize,'\n' #Net meaning after Spanish and Non-English-Unicode-Only tweets are filtered.


#Writes the information to a csv file ready for import to GraphLab.
#fileName is the desired fileName for the output.
#pairs is the dictionary with the pair information.

#Outputs three CSVs: 
#	<name>_v.csv -Vertex List
#	<name>_e.csv -Edge List
#	<name>_e_wNames.csv -Edge List with the Word Names rather than id numbers.
#And an info.txt
def write_CSV(fileName, corpus, pairs):

	#Set file paths.
	vertexPath = fileName+"_v.csv";
	edgePath = fileName+"_e.csv";
	wnamesPath = fileName+"_e_wNames.csv";
	infoPath = fileName+"_info.txt";

	#Keep track of vertex IDs.
	vertId = dict();

	#<name>_v.csv -Vertex List
	with open(vertexPath, 'w') as vertF:
		vertHeaders = ['id', 'word'];
		csvWriter = csv.writer(vertF)
		csvWriter.writerow(vertHeaders)

		for index, vert in enumerate(corpus):
			vertId[vert] = index;
			line = [index, vert.encode('UTF-8','xmlcharrefreplace')]
			csvWriter.writerow(line);

	#<name>_e.csv -Edge List
	with open(edgePath, 'w') as edgeF:
		edgeHeaders = ['Word 1', 'Word 2', 'Co-occurrence']
		csvWriter = csv.writer(edgeF)
		csvWriter.writerow(edgeHeaders)

		for pair, count in pairs.iteritems():
			wordOne, wordTwo = pair.split('\t')
			line = [vertId.get(wordOne), vertId.get(wordTwo), count]
			csvWriter.writerow(line)

	#<name>_e_wNames.csv -Edge List with the Word Names rather than id numbers.
	with open(wnamesPath, 'w') as edgeF:
		edgeHeaders = ['Word 1', 'Word 2', 'Co-occurrence']
		csvWriter = csv.writer(edgeF)
		csvWriter.writerow(edgeHeaders)

		for pair, count in pairs.iteritems():
			wordOne, wordTwo = pair.split('\t')
			line = [wordOne, wordTwo, count]
			csvWriter.writerow(line)

	with open(infoPath,'w') as infoFile:
		global corpusSize
		infoFile.write('Net number of tweets: ')
		infoFile.write(str(corpusSize))

	print "\nWriting complete.\n\n"


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

#Main Logic
def main():
	#Mongo Setup
	dbclient = MongoClient('z')
	db = dbclient.new_boston
	mongo_config = db.tweets
	tweetIter = randomMongo(mongo_config)

	#Get destination path from the user.
	fName = raw_input('Destination file name: ')

	#Build Graph.
	corpus_from_mongo(tweetIter, fName)

	exit()


main()
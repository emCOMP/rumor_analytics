import csv
import re
from pymongo import MongoClient
from nltk.corpus import stopwords

# Helper for processTweets
def clean_tweet(tweetText):
    # Convert to unicode.
    # Must encode then re-encode because of some funky mixing of strings and
    # unicode in tweets.
    pTweet = tweetText.encode('UTF-8', 'ignore').decode('UTF-8', 'ignore')
    pTweet = re.sub(r'@\w+', u'', pTweet)
    # Remove URLs
    pTweet = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', u'', pTweet)
    # Remove punctuation
    pTweet = re.sub(r'\n|rt|RT|[!#$%&"()*+,\-./:;<=>?@\[\\\]^_`{|}~]', u'', pTweet)
    # Remove Non-ASCII Unicode
    pTweet = re.sub(r"[^\x00-\x7F]+|'", u'', pTweet).lower()
    #Remove Stopwords
    pTweet = ' '.join([w for w in pTweet.split() if w not in stops])

    return pTweet

# DB Setup
dbclient = MongoClient('z')
db = dbclient.amtrak
q = {'$and':[{'text':{'$regex':'mph|speed|sped|accelerate|fast','$options':'i'}},{'text':{'$regex':'turn|curve','$options':'i'}}]}
tweetIter = db.tweets.find(q, {"text": 1,"user":1,"created_ts":1,"retweeted":1,"lang":1})
'''
filter_words = set(stopwords.words())
# Remove the english stopwords from the filter.
filter_words.difference_update(set(stopwords.words('english')))
filter_words = frozenset(filter_words)
'''
stops = frozenset(stopwords.words('english'))


with open('amtrak_spedup_dump.csv', 'wb') as f:
    f_writer = csv.writer(f)
    for t in tweetIter:
        text = clean_tweet(t['text'])
        #other_language = any([True for w in text.split() if w in filter_words])
        english = (t['lang'].lower() == 'en')

        if english:
        	f_writer.writerow([str(t['_id']),text,t['user']['id_str'],str(t["created_ts"]),t["retweeted"]])

print 'Success!'

exit()

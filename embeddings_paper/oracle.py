import gensim
import json
import time
from nltk.stem.snowball import EnglishStemmer
from pymongo import MongoClient

def user_select(choices):
	for i,e in enumerate(choices):
		print str(i)+'.\t',e

	print '\nPlease choose new search terms.'
	#Get user choices
	usr_choices = []
	usr_in = str(raw_input('Enter choices by number:')).strip()
	while usr_in != 'DONE':
		usr_choices.append(choices[int(usr_in)][0])
		usr_in = str(raw_input('("DONE" when finished):')).strip()
	print 'Selections: ',usr_choices,'\n'
	return usr_choices

#Mongo Setup
dbclient = MongoClient('z')
db = dbclient.new_boston
mongo = db.tweets

#Initialization
p = raw_input('Path to embeddings:').strip()
print 'Loading...'
model = gensim.models.Word2Vec.load_word2vec_format(p,binary=True)
print 'Initializing...'
model.init_sims(replace=True)

#Get seed terms
seeds = []
stemmer = EnglishStemmer(True)
usr_in = str(raw_input('Please enter seed terms one at a time:')).strip()
while usr_in != 'DONE':
	seeds.append(stemmer.stem(usr_in)) #Append a stemmed version of the word.
	usr_in = str(raw_input('("DONE" when finished):')).strip()


print '\nFinding new terms...'
#This will store all of the seed terms and the corresponding lists of 'interesting terms'.
seed_lists = {}
for seed in seeds:
	print '='*40,'\n','Seed Term: ',seed,'\n','='*40,'\n'

	if seed in model:
		#Get the top n most similar word vectors.
		nearest = model.most_similar(positive=[seed])
		
		#Store list of user-selected 'interesting terms' in dictionary.
		seed_lists[seed] = user_select(nearest)

	else:
		print 'Seed term: "'+seed+'" is not in the corpus. Skipping...' 


print 'Showing new query results:'
revised_lists = {}
#Have the user examine what each term does to the search results.
for seed,term_list in seed_lists.iteritems():
	print '='*40,'\n','Seed Term: ',seed,'\n','='*40,'\n'
	
	#A list to store the 'interesting terms'
	#which the user decides to keep.
	cur_revised_list = []

	#A list of and statements.
	ands = []
	for term in term_list:
		print '\tNew Term: ',term,'\n\t','-'*30,'\n'
		#Make a new copy of the ands list with our current term added.
		cur_ands = [{'$and':[{'text':{'$regex':seed, '$options':'i'}},{'text':{'$regex':term, '$options':'i'}}]}]
		cur_ands.extend(ands)

		cursor = mongo.find({"$or":cur_ands},{'_id':0,'text':1}).limit(10)
		time.sleep(2)
		for result in cursor:
			print result['text'],'\n'

		#Get the user's response.
		keep = ''
		while (keep != 'y' and keep != 'n'):
			keep = raw_input('\n\tKeep this new term?(y/n):').strip()

		#If the user wants to keep the term, add it to the query.
		#And to the new term list.
		if keep == 'y':
			ands.append(cur_ands[0])
			cur_revised_list.append(term)


	revised_lists[seed] = cur_revised_list

query = {'$or':[{'text':{'$regex':t, '$options':'i'}} for t in revised_lists.keys()]}
print '='*40,'\n','Final Lists\n', '='*40
for k,v in revised_lists.iteritems():
	print k,'\t',v

	cur_ands = [({'$and':[{'text':{'$regex':k, '$options':'i'}},{'text':{'$regex':term, '$options':'i'}}]}) for term in v]
	prev_or = query['$or']
	prev_or.extend(cur_ands)
	query['$or'] = prev_or

final_q = json.dumps(query)
print 'Final Query:\n'
print final_q

with open('oracle_query.txt','ab') as f:
	f.write(final_q)

exit()

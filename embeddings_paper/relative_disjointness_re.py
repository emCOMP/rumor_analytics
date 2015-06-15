import gensim
import json
import pprint
import re
from pymongo import MongoClient
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords

TOP_N = 10
MAX_DEPTH = 2

EVENT_TERMS = ['sydneysiege',
					'martinplacesiege',
					'haron',
					'monis',
					'haronmonis',
					'illridewithyou',
					'martinplace',
					'Sydney',
					'chocolate shop',
					'nswpolice',
					'prime minister',
					'tony abbott',
					'witness',
					'lindt',
					'siege',
					'hostage',
					'hostages',
					'martin place',
					'terrorise',
					'terrorize',
					'terrorists',
					'flag'
				]

#Stems all terms in the input.
#(Handles multi-word inputs)
def clean_input(usr_in):
	tmp = usr_in.split(' ')
	tmp = map(stemmer.stem, tmp)
	result = ' '.join(tmp)
	return result

#Queries the user for seed terms and returns a list of seed strings.
def get_seeds(cutoff):
	seeds = []

	#Get user input.
	print 'Please enter OR terms one at a time.\n To enter AND terms: type them in the same entry serparated by a space.'
	print 'Example: Apple OR Orange = Apple [press enter] Orange, Apple AND Orange  = Apple Orange'
	usr_in = str(raw_input('Please enter seed terms one at a time:')).strip()
	
	while usr_in != 'DONE':
		seeds.append(clean_input(usr_in)) #Append a stemmed version of the word.
		usr_in = str(raw_input('("DONE" when finished):')).strip()

	return seeds


#Takes a list of seed strings.
#Returns a dictionary where keys are seed terms and values are a list of candidate terms.
#Returns a set 'u' which consists of all candidate terms.
def get_candidates(seeds, cutoff, prev=[]):
	
	#---Initialize the structures for the return data.
	seed_dict = {s:[] for s in seeds} #This line needs to come before the splitting below.
	u = set()	

	#---Split any 'and' terms that get passed in.
	prev_terms = []
	for p in prev:
		prev_terms.extend(p.split(' '))
	
	seeds = [s.split(' ') for s in seeds]

	#---Find candidate terms.
	for seed in seeds:	
		#Make sure all of the seeds are in the model.	
		seed_in_model = all([bool(i in model) for i in seed])
		if seed_in_model:
			#print seed+prev_terms
			
			#Find terms similar to the current seed string, plus any 'previous terms'
			#(Previous meaning terms which are ANDed with the current seed.)
			result = model.most_similar_cosmul(positive=seed+prev_terms,topn=TOP_N)
			nearest_terms = [r[0] for r in result if r[1] >= cutoff and\
							 r[0] not in seeds and\
							 r[0] not in stops and\
							 r[0] not in prev_terms ]

			#Store the top n most similar in the dictionary.
			seed_key = ' '.join(seed)
			seed_dict[seed_key].extend(nearest_terms)

			#Add the terms to u.
			u = u.union(set(nearest_terms))

		#Otherwise print an error.
		else:
			print 'Seed term: "'+str(seed)+'" is not in the model. Skipping...'
	#print 'Dict:\t',seed_dict
	#print 'U:\t',u
	return (seed_dict,u)


#Takes a list of terms to be ANDed
#inner_val is the value to place at the inner-most level of the dictionary.
#(This will be the value corresponding to the last element of the chain which is passed in.)
#i is the current recursion depth
#returns an appropriate dictionary.
def chain_to_dict(chain, inner_val=[], i=0):
	#print i,'\t',chain
	if i < len(chain) - 1:
		return {chain[i]:chain_to_dict(chain, inner_val=inner_val, i=i+1)}
	else:
		return {chain[i]:inner_val}

#Recursive helper for expand()
def _expand(seeds, cutoff, prev_terms=[],depth=0):

	##Get candidate terms to be introduced into the query.
	#candidates is a dict where keys are or_terms and values are lists of candidate terms for that seed.
	#u is a set containing the union of all words in candidates.
	candidates, u = get_candidates(seeds, cutoff, prev_terms)


	#---Now we need to decide which terms should be ANDed,
	#	which should be ORed, and which to throw out.
	#	ORs will be new keys in the current dict, 
	#	ANDs will be keys inside a new dict (which will be a value in the current dict). 
	or_terms = seeds
	new_terms = [0] #Needs to have at least one element to prime the loop.
	
	#---Find OR Terms
	#Keep expanding the list of OR terms until no new terms are returned.
	while len(new_terms) > 0:
		print 'Expanding results...'
		new_terms = []

		for t in u:
			#Count how many lists this appears in.
			appears_in = [seed for seed,l in candidates.iteritems() if t in l]
			#What percentage of the lists did this term appear in?
			percent = float(len(appears_in))/len(candidates.keys())
			if percent >= x and t not in or_terms:
				#Add it to the or terms.
				or_terms.append(t)
				new_terms.append(t)
		
		#If there are any new terms.
		if len(new_terms):
			#Get new candidates with the new or_terms and update u.
			candidates, new_u = get_candidates(new_terms, cutoff)
			u = u.union(new_u)


	#---Find AND terms.
	next_layer = {k:[] for k in candidates.keys()}
	print 'Refining...'
	for t in u:
		#Count how many lists this appears in.
		appears_in = [seed for seed,l in candidates.iteritems() if t in l]
		
		#What percentage of the lists did this term appear in?
		#percent = float(len(appears_in))/len(seed_lists.keys())			
		#print t,'\t',percent

		#If the term appears in only one or two candidate lists, add it as an AND term
		#for the seeds corresponding to those lists.
		if len(appears_in) <= 2 and t not in or_terms and t not in prev_terms:
			for k in appears_in:
				next_layer[k].append(t)

	#---Recurse
	#For each seed-term which has AND terms, apply this method to each AND term.
	for k,v in next_layer.iteritems():
		if len(v) > 0 and depth < MAX_DEPTH:
			next_layer[k] = _expand(v,cutoff,prev_terms+[k], depth=depth+1)

	print '\nCurrent Terms:'
	pprint.pprint(next_layer, width=1, depth=depth+1)
	print '\n','-'*40
	return next_layer


#Takes a list of seed strings 'seeds' and a minimum cosine distance 'cutoff'
#Returns a dictionary where keys are 'ORed' terms, and values are other dictionaries of the same format.
def expand(seeds, cutoff):

	result = _expand(seeds,cutoff)
	for s in seeds:
		result.setdefault(s,[])

	#Convert any multi-word terms into ANDs.
	for k in result.keys():
		spl = k.split(' ')
		
		#Convert the multi-word key into a dictionary with multiple single-word keys.
		if len(spl) > 1:		
			true_seed = spl[0] #The first word in the AND chain.
			chain_dict = chain_to_dict(spl,inner_val=result[k],i=1)

			#If the single-word key is not in result, add an empty dictionary.
			if true_seed not in result or type(result[true_seed]) == list:
				result[true_seed] = {}

			#Update the single-word key's value.
			result[true_seed].update(chain_dict) #!!!!!!!!!!!If terms go missing, this line might be causing it.
			#Remove the multi-word key.
			del result[k]

	return result


'''
def _explore_branches(seed_dict):
	final_result = []
	for k,v in seed_dict.iteritems():
		k_reg = {'text':{'$regex':k, '$options':'i'}}
		if type(v) == dict:
			result = [k_reg{'$or':_explore_branches(v)}]
		elif type(v) == list:
			result = [k_reg, {'text':{'$regex':'|'.join(map(str,v)), '$options':'i'}}]
		else:
			print 'Error, unexpected type:\t', type(v)

		final_result.append(result)
	
	return final_result
'''

'''
def _explore_branches(seed_dict):
	result = []
	
	for k,v in seed_dict.iteritems():
		k_reg = {'text':{'$regex':k, '$options':'i'}}
		if type(v) == dict:
			if len(v) > 1:
				result.append([k_reg,{'$or':_explore_branches(v)}])
			elif len(v) == 1:
				result.append([k_reg,_explore_branches(v)])
		
		elif type(v) == list:
			if len(v):
				result.append([k_reg, {'text':{'$regex':'|'.join(map(str,v)), '$options':'i'}}])
			else:
				result.append(k_reg)

	return result

def _dict_to_query(seed_dict):
	roots = []
	
	for k,v in seed_dict.iteritems():
		root_q = {'text':{'$regex':k, '$options':'i'}}
		
		if len(v):
			branches = _explore_branches(v)
			pprint.pprint(branches)
			q = {'$and':[root_q]+branches}
		else:
			q = root_q

		roots.append(q)

	return roots
'''


#####
def _dict_to_query(seed_dict):
	q = []
	for k,v in seed_dict.iteritems():
		cur = [{'text':{'$regex':k, '$options':'i'}}]
		#cur = [{'text':re.compile(k,re.IGNORECASE)}]
		if type(v) == dict:
			if len(v) > 1:
				tmp = [{'$and':x} if type(x) == list else x for x in _dict_to_query(v)]
				cur.append({'$or':tmp})
			elif len(v) == 1:
				cur.extend(_dict_to_query(v))
		elif type(v) == list:
			if len(v):
				cur.append({'text':{'$regex':'|'.join(map(str,v)), '$options':'i'}})
				#cur.append({'text':re.compile('|'.join(map(str,v)),re.IGNORECASE)})
		
		if len(cur) == 1:
			cur = cur[0]
		elif len(cur) == 0:
			cur = None
		else:
			cur = {'$and':cur}
		
		q.append(cur)

	final_q =[]
	for i in q:
		if type(i) == list:
			final_q.extend(i)
		else:
			final_q.append(i)
	
	return final_q


def dict_to_query(seed_dict):
	result = _dict_to_query(seed_dict)
	if len(result) > 1:
		return {'$or':result}
	else:
		return result[0]


##################################################################################
#---Initialization
#p = raw_input('Path to embeddings:').strip()
p = 'sydney_fixed.bin'
print 'Loading...'
model = gensim.models.Word2Vec.load_word2vec_format(p,binary=True)
print 'Initializing...'
model.init_sims(replace=True)
stemmer = EnglishStemmer(True)
stops = set(stopwords.words('english'))
stops.add('rt')
stops.add('http')
stops = stops.union(set(map(stemmer.stem,EVENT_TERMS)))
stops = frozenset(stops)

#---Set parameters.
x = float(raw_input('x (0.6 reccomended): '))
#x = 0.5
cutoff = float(raw_input('Minimum cosine similarity (0.5 reccomended): '))
#cutoff = 0.5

#---Get the query.
seeds = get_seeds(cutoff)
result = expand(seeds, cutoff)

#---Construct the final query.
print 'Constructing final query...'
query = dict_to_query(result)
final_q = json.dumps(query, sort_keys=True,indent=4, separators=(',', ': '))

print 'Final Query:','\n',final_q

#---Save the query to a file.
with open('relative_disjointness_query.txt','wb') as f:
	f.write(final_q)

#---Test the query.
#########Mongo Setup
dbclient = MongoClient('z')
db = dbclient.sydneysiege
mongo = db.tweets

print '\nQuery Results:\n'
cursor = mongo.find(query,{'text':1,'_id':0}).limit(25)

for i,v in enumerate(cursor):
	print i+1,'\t',v['text']

exit()
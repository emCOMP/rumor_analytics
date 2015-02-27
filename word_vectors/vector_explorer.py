import gensim
import logging
import numpy as np

#model.index2word[index]

#Ego is the word to find similarities for.
#Model is the Word2Vec model.
def get_axis_words(ego, model):
	if ego in model:
		ego_vector = model[ego]
		ego_index = model.vocab[ego].index
		closest_on_axis = [-1]*len(ego_vector)

		#For each component of the vector(i), we'll find the other vector nearest to it in that axis.
		for i, v in enumerate(ego_vector):
			#The index of the word closest on this axis.
			closest_index = -1
			closest_diff = 2.0


			for j, w in enumerate(model.syn0):
				if j == ego_index:
					continue
				else:		
					cur_diff = abs(v - w[i])
					if cur_diff < closest_diff:
						closest_index = j
						closest_diff = cur_diff

			closest_on_axis[i] = closest_index

		#Return the words, not the indices.
		return map(lambda x: model.index2word[x], closest_on_axis)

	else:
		return ['Word not in dict.']



logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
model = gensim.models.Word2Vec.load_word2vec_format('data/embeddings/GoogleNews-vectors.bin.gz',binary=True)
model.init_sims(replace=True)

usr_in = str(raw_input('Word to search ("EXIT" to quit):')).strip()
#n = int(raw_input('How many similar words per axis? '))

while usr_in != 'EXIT':

	nearest_by_axis = get_axis_words(usr_in, model)
	print 'Word: '+usr_in+'\n'
	print 'Axis\tNearest Word'
	print '-'*30
	for i,v in enumerate(nearest_by_axis):
		print str(i+1)+'\t'+v

	print '-'*30

	usr_in = str(raw_input('Word to search ("EXIT" to quit):')).strip()
	#n = int(raw_input('How many similar words per axis? '))
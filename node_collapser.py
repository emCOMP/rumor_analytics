'''
This script collapses the nodes of a given graph based on word-embedding distance.
'''

import graphlab as gl
from nltk.stem.snowball import EnglishStemmer

words = None

with open('data/embeddings/vocab.txt', 'rb') as f:
	vocab = f.read().splitlines()
	words = gl.SArray(data=vocab)

#Stem the words so they line up with our stemmed words.
stemmer = EnglishStemmer(True)
words = words.apply(lambda x: stemmer.stem(x))

embeddings = gl.SFrame.read_csv(url='data/embeddings/100d.txt', delimiter=' ', header=False, column_type_hints=float)
embeddings = embeddings.add_column(words,'word')
embeddings = embeddings.swap_columns(embeddings.column_names()[0], 'word')

print 'Embeddings import complete.\n'
embeddings.head()

#Import our graph.
frame = gl.SFrame.read_csv('csv/boston_no_subjectives_e_wNames.csv',True)

print 'Graph import complete.\n'
frame.head()


print 'Words will be collapsed with k nearest-neighbors.\nk: '
k = int(raw_input())



print 'Filtering embeddings...'
temp1 = embeddings.filter_by(frame.select_column('Word 1'), 'word')
temp2 = embeddings.filter_by(frame.select_column('Word 2'), 'word')

#Only the embeddings for the words present in our graph.
filtered_embeddings = temp1.append(temp2).unique()

print 'Filtering complete.\n'
filtered_embeddings.head()

print 'Calculating nearest-neighbors...'
nearest_m = gl.nearest_neighbors.create(embeddings, label='word')
nearest = nearest_m.query(filtered_embeddings, label='word',k=k)

#print '\nCollapsing nodes...'




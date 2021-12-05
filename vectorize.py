from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.manifold import TSNE, Isomap, SpectralEmbedding
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import LatentDirichletAllocation, PCA, NMF, TruncatedSVD
from sklearn.preprocessing import scale, normalize
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.cluster import AgglomerativeClustering
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import numpy as np
import json
import os
import re
import sys
import pickle

stop_word_list = [
    "s","t","'s","n't",'m',"'m","'ve","'re","'ll",'re',"'d","ve",
    '(',')','[',']',':',',','.','’','“','”','``',"''",'&',';','?','-',"'",'!','↩︎','—','...','--','*','‘','–',
    'a','about','all','also','an','am','and','are','as','at','be','been','but','by','can','could','did','do','doing','for','from','had','has','have','he','her','him','his','how',
    'i','if','in','into','is','it','its','like','may','me','might','more','my','not','some','no','of','on','one','or','other','our','out',
    'said','she','should','so','such','than','that','the','their','them','then','there','these','they','this','to','up','us',
    'very','was','we','were','what','when','where','which','who','will','with','would','you','your',

    'because','even','get','just','know','make','many','most','much','people','really','something','think','thing','things','time','want','way',
]

def main():
    print('loading and cleaning html...')
    all_docs = []
    all_titles = []
    for path in sorted(os.listdir(path='data')):
        with open(f'data/{path}') as f:
            obj = json.load(f)
            all_docs.append(BeautifulSoup(obj['body'], features='html.parser').get_text())
            all_titles.append(obj['title'])
    print(f'Total document count (including ones we\'ll reject: {len(all_docs)}')
    print('tokenizing...')
    word_counts = []
    titles = []
    docs = []
    re_word = re.compile('[-a-zA-Z]+')
    for i in range(len(all_docs)):
        tokens = word_tokenize(all_docs[i])
        if len(tokens) >= 100:
            word_counts.append(len(tokens))
            #docs.append(' '.join(filter(lambda t:re_word.match(t), tokens)))
            docs.append(' '.join(tokens))
            titles.append(all_titles[i])

    all_docs = None
    n = len(docs)
    print(n)
    print('vectorizing...')
    vectorizer = TfidfVectorizer(stop_words=stop_word_list, tokenizer=lambda x:x.split())
    reducer = VarianceThreshold(threshold = 0.0001)
    X = vectorizer.fit_transform(docs)
    word_counts = np.sum(X, axis=1)
    feature_names = vectorizer.get_feature_names_out()
    print(len(feature_names))
    print(X.shape)
    print('feature selection')
    X_reduced = reducer.fit_transform(X)
    feature_names_reduced = reducer.get_feature_names_out(feature_names)
    print(X_reduced.shape)

    print('pickling...')
    p = (X_reduced, feature_names_reduced, titles, word_counts)
    with open('xreduced.pickle', 'wb') as f:
        pickle.dump(p, f)


if __name__ == '__main__':
    main()

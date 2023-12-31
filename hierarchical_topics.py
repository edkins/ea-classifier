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
import pickle
import re
import sys

def main():
    print('unpickling...')
    with open('xreduced.pickle','rb') as f:
        X_reduced, feature_names_reduced, titles, word_counts = pickle.load(f)

    n = X_reduced.shape[0]

    print('non-negative matrix factorization')
    n_topics = int(sys.argv[1])
    perplexity = int(sys.argv[2])
    nmf = NMF(n_topics)
    X_nmf = nmf.fit_transform(X_reduced)

    topics = []
    for i in range(n_topics):
        topic = []
        for j in range(len(feature_names_reduced)):
            word = feature_names_reduced[j]
            value = nmf.components_[i, j]
            topic.append([word, value])
        topic.sort(key=lambda wv: wv[1], reverse=True)
        topics.append(topic[:30])

    print('calc relatedness')
    relatedness = np.matmul(np.transpose(X_nmf), X_nmf)
    print(relatedness.shape)
    
    print('tsne on topics...')
    xy = scale(TSNE(2,perplexity=perplexity).fit_transform(np.power(np.transpose(X_nmf),0.3))) * 0.5

    with open('output.json','w') as f:
        f.write(json.dumps({
            'x': [float(x) for x in xy[:,0]],
            'y': [float(y) for y in xy[:,1]],
            'topics': topics,
            'titles': titles,
            'topicality': [[float(t) for t in top] for top in X_nmf],
            'relatedness': [[float(r) for r in rel] for rel in relatedness],
        }, indent=4))


if __name__ == '__main__':
    main()

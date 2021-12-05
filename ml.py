from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.manifold import TSNE
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import LatentDirichletAllocation, PCA, NMF
from sklearn.preprocessing import normalize
from bs4 import BeautifulSoup
import numpy as np
import json
import os

def main():
    print('loading and cleaning html...')
    docs = []
    titles = []
    for path in sorted(os.listdir(path='data')):
        with open(f'data/{path}') as f:
            obj = json.load(f)
            if len(obj['body']) > 1000:
                docs.append(BeautifulSoup(obj['body'], features='html.parser').get_text())
                titles.append(obj['title'])
    print(len(docs))
    print('vectorizing...')
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(docs)
    word_counts = np.sum(X, axis=1)
    feature_names = vectorizer.get_feature_names_out()
    print(len(feature_names))
    print(X.shape)
    print('feature selection')
    reducer = VarianceThreshold(threshold = 0.0001)
    X_reduced = reducer.fit_transform(X)
    feature_names_reduced = reducer.get_feature_names_out(feature_names)
    print(X_reduced.shape)
    print('latent dirichlet allocation...')
    n_topics = 10
    lda = NMF(n_components=n_topics)
    X_lda = lda.fit_transform(X_reduced)
    print(X_reduced.shape)
    #print('tsne...')
    xy = TSNE(n_components=2, init='random', verbose=2, perplexity=30).fit_transform(X_lda)
    #xy = PCA(2).fit_transform(X_reduced)
    print(xy.shape)
    print('writing as json...')

    topics = []
    for i in range(n_topics):
        topic = []
        for j in range(len(feature_names_reduced)):
            word = feature_names_reduced[j]
            value = lda.components_[i, j]
            topic.append([word, value])
        topic.sort(key=lambda wv: wv[1], reverse=True)
        topics.append(topic[:10])

    with open('output.json','w') as f:
        f.write(json.dumps({
            'x': [float(x) for x in xy[:,0]],
            'y': [float(y) for y in xy[:,1]],
            'topicality': [[float(t) for t in top] for top in X_lda],
            'titles': titles,
            'word_counts': [int(c) for c in word_counts],
            'keywords': [str(n) for n in feature_names_reduced],
            'topics': topics
        }, indent=4))


if __name__ == '__main__':
    main()

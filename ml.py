from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.manifold import TSNE, Isomap, SpectralEmbedding
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import LatentDirichletAllocation, PCA, NMF, TruncatedSVD
from sklearn.preprocessing import scale, normalize
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from bs4 import BeautifulSoup
import numpy as np
import json
import os
import sys

if len(sys.argv) >= 3:
    method = sys.argv[1]
    method2 = sys.argv[2]
    n_topics = int(sys.argv[3])
else:
    method = 'nmf-kl'
    method2 = 'tsne_graph'
    n_topics = 20

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
    if method in ['lda']:
        vectorizer = CountVectorizer(stop_words='english')
        reducer = VarianceThreshold(threshold = 0.1)
    elif method in ['nmf','nmf-kl']:
        vectorizer = TfidfVectorizer(stop_words='english')
        reducer = VarianceThreshold(threshold = 0.0001)
    else:
        raise Exception(f'Unknown method: {method}')
    X = vectorizer.fit_transform(docs)
    word_counts = np.sum(X, axis=1)
    feature_names = vectorizer.get_feature_names_out()
    print(len(feature_names))
    print(X.shape)
    print('feature selection')
    X_reduced = reducer.fit_transform(X)
    feature_names_reduced = reducer.get_feature_names_out(feature_names)
    print(X_reduced.shape)
    if method == 'lda':
        print('latent dirichlet allocation...')
        lda = LatentDirichletAllocation(n_components=n_topics)
    elif method == 'nmf':
        print('nonnegative matrix factorization')
        lda = NMF(n_components=n_topics)
    elif method == 'nmf-kl':
        print('nonnegative matrix factorization (kullback-leibler)')
        lda = NMF(n_components=n_topics, beta_loss='kullback-leibler', solver='mu')
    else:
        raise Exception(f'Unknown method: {method}')
    X_lda = lda.fit_transform(X_reduced)
    print(X_lda.shape)
    if method2 == 'tsne':
        print('tsne...')
        xy = TSNE(n_components=2, init='random', verbose=2, perplexity=30).fit_transform(X_lda)
    elif method2 == 'tsne_graph':
        print('tsne...')
        graph = X_lda / np.reshape(np.sum(X_lda, axis=1), (X_lda.shape[0], 1))
        xy = TSNE(n_components=2, init='random', verbose=2, perplexity=30).fit_transform(graph)
    elif method2 == 'pca':
        print('pca...')
        xy = PCA(n_components=2).fit_transform(X_lda)
    elif method2 == 'isomap':
        print('isomap...')
        xy = Isomap(n_components=2).fit_transform(X_lda)
    elif method2 == 'se':
        print('spectral embedding...')
        xy = SpectralEmbedding(n_components=2).fit_transform(X_lda)
    elif method2 == 'circle':
        print('dumb circle embedding...')
        circle = np.array([[np.cos(t * 6.283 / n_topics), np.sin(t * 6.283 / n_topics)] for t in range(n_topics)])
        xy = np.matmul(X_lda, circle)
    elif method2 == 'circle_graph':
        print('dumb circle graph embedding...')
        graph = X_lda / np.reshape(np.sum(X_lda, axis=1), (X_lda.shape[0], 1))
        circle = np.array([[np.cos(t * 6.283 / n_topics), np.sin(t * 6.283 / n_topics)] for t in range(n_topics)])
        xy = np.matmul(graph, circle)
    elif method2 == 'topic':
        print('placing topics...')
        topic_xy = PCA(n_components=2).fit_transform(lda.components_)
        xy = np.matmul(X_lda, topic_xy)
    elif method2 == 'topic_circle':
        print('placing topics around circle...')
        topic_xy = PCA(n_components=2).fit_transform(lda.components_)
        topic_xy = normalize(topic_xy)
        xy = np.matmul(X_lda, topic_xy)
    elif method2 == 'lda':   # the other kind of lda
        print('linear discriminant analysis...')
        labels = np.argmax(X_lda, axis=1)
        X_further_reduced = TruncatedSVD(n_components=100).fit_transform(X_reduced)
        xy = LinearDiscriminantAnalysis(n_components=2).fit_transform(X_further_reduced, labels)
    else:
        raise Exception(f'Unknown method2: {method2}')
    xy = scale(xy)
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

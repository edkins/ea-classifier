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

class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def split(self, gap, ratio):
        r1 = 1 - ratio
        if self.w > self.h:
            return Rect(self.x, self.y, self.w * ratio - gap, self.h), Rect(self.x + self.w * ratio + gap, self.y, self.w * r1 - gap, self.h)
        else:
            return Rect(self.x, self.y, self.w, self.h * ratio - gap), Rect(self.x, self.y + self.h * ratio + gap, self.w, self.h * r1 - gap)

def visit_node_counts(output, agglom, n, node_index):
    if node_index < n:
        output[node_index] = 1
        return 1
    else:
        n0 = visit_node_counts(output, agglom, n, agglom.children_[node_index - n, 0])
        n1 = visit_node_counts(output, agglom, n, agglom.children_[node_index - n, 1])
        output[node_index] = n0 + n1
        return n0 + n1

def visit_node(output, agglom, n, titles, counts, node_index, depth, rect):
    if node_index < n:
        #print(f'{"-" * depth} [{agglom.labels_[node_index]}] {titles[node_index]}')
        output['x'].append(rect.x)
        output['y'].append(rect.y)
        output['titles'].append(titles[node_index])
    else:
        distance = agglom.distances_[node_index - n]
        #print(f'{"-" * depth} {distance}')
        gap = min(distance / 100, rect.w * 0.5, rect.h * 0.5)
        i0 = agglom.children_[node_index - n, 0]
        i1 = agglom.children_[node_index - n, 1]
        n0 = float(counts[i0])
        n1 = float(counts[i1])
        rect0, rect1 = rect.split(gap, n0 / (n0 + n1))
        visit_node(output, agglom, n, titles, counts, i0, depth + 1, rect0)
        visit_node(output, agglom, n, titles, counts, i1, depth + 1, rect1)

def main():
    print('unpickling...')
    with open('xreduced.pickle','rb') as f:
        X_reduced, feature_names_reduced, titles, word_counts = pickle.load(f)

    n = X_reduced.shape[0]

    print('agglomerative clustering')
    n_clusters = 50
    agglom = AgglomerativeClustering(n_clusters, compute_distances=True)
    clusters = agglom.fit_predict(X_reduced.toarray())

    output = {'x':[], 'y':[], 'titles':[]}
    counts = np.zeros((2 * n - 1,))
    print('tree crawling and point placement')
    visit_node_counts(counts, agglom, n, 2 * n - 2)
    visit_node(output, agglom, n, titles, counts, 2 * n - 2, 0, Rect(-1, -1, 2, 2))

    print('writing output')
    with open('output.json', 'w') as f:
        json.dump(output, f)
    print(len(output['titles']))


if __name__ == '__main__':
    main()

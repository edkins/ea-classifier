from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
from sklearn.feature_selection import VarianceThreshold
from bs4 import BeautifulSoup
import json
import os

def main():
    print('loading and cleaning html...')
    docs = []
    titles = []
    for path in sorted(os.listdir(path='data')):
        with open(f'data/{path}') as f:
            obj = json.load(f)
            docs.append(BeautifulSoup(obj['body'], features='html.parser').get_text())
            titles.append(obj['title'])
    print(len(docs))
    print('vectorizing...')
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(docs)
    feature_names = vectorizer.get_feature_names_out()
    print(len(feature_names))
    print(X.shape)
    print('feature selection')
    reducer = VarianceThreshold(threshold = 0.001)
    X_reduced = reducer.fit_transform(X)
    feature_names_reduced = reducer.get_feature_names_out(feature_names)
    print(X_reduced.shape)
    print('tsne...')
    tsne = TSNE(n_components=2, init='random', verbose=2, perplexity=30)
    xy = tsne.fit_transform(X_reduced)
    print(xy.shape)
    print('writing as json...')
    with open('output.json','w') as f:
        f.write(json.dumps({
            'x': [float(x) for x in xy[:,0]],
            'y': [float(y) for y in xy[:,1]],
            'titles': titles,
            'keywords': [str(n) for n in feature_names_reduced]
        }, indent=4))


if __name__ == '__main__':
    main()

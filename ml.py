from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
import json
import os

def main():
    docs = []
    titles = []
    for path in sorted(os.listdir(path='data')):
        with open(f'data/{path}') as f:
            obj = json.load(f)
            docs.append(obj['body'])
            titles.append(obj['title'])
    print(len(docs))
    print('vectorizing...')
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(docs)
    print(len(vectorizer.get_feature_names_out()))
    print(X.shape)
    print('tsne...')
    tsne = TSNE(n_components=2, init='random', verbose=2, perplexity=30)
    xy = tsne.fit_transform(X)
    print(xy.shape)
    print('writing as json...')
    with open('output.json','w') as f:
        f.write(json.dumps({
            'x': [float(x) for x in xy[:,0]],
            'y': [float(y) for y in xy[:,1]],
            'titles': titles
        }, indent=4))


if __name__ == '__main__':
    main()

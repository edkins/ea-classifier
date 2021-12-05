import json
import matplotlib.pyplot as plt
import numpy as np

def main():
    with open('output.json') as f:
        obj = json.load(f)
    x = obj['x']
    y = obj['y']
    c = np.log(obj['word_counts'])
    plt.scatter(x=x, y=y, c=c)
    plt.show()

if __name__ == '__main__':
    main()

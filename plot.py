import json
import matplotlib.pyplot as plt
import numpy as np

def main():
    with open('output.json') as f:
        obj = json.load(f)
    x = obj['x']
    y = obj['y']
    c = np.argmax(obj['topicality'], axis=1)
    plt.scatter(x=x, y=y, c=c, cmap='tab10')
    plt.show()

if __name__ == '__main__':
    main()

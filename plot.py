import json
import matplotlib.pyplot as plt

def main():
    with open('output.json') as f:
        obj = json.load(f)
    x = obj['x']
    y = obj['y']
    plt.scatter(x=x, y=y)
    plt.show()

if __name__ == '__main__':
    main()

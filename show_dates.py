from collections import defaultdict
import json
import os

def main():
    dates = defaultdict(int)
    for path in os.listdir(path='data'):
        with open(f'data/{path}') as f:
            obj = json.load(f)
            date = obj['datePosted'][:10]
            dates[date] += 1
    for date in sorted(dates.keys()):
        print(f'{date}: {dates[date]}')

if __name__ == '__main__':
    main()

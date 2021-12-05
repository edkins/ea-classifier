import json

def main():
    with open('output.json') as f:
        obj = json.load(f)
    topics = obj['topics']
    for i in range(len(topics[0])):
        string = ''
        for j in range(len(topics)):
            string += f'{topics[j][i][0]:20}'
        print(string)


if __name__ == '__main__':
    main()

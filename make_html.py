import sys

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'template.t'

    with open('output.json') as f:
        data = f.read()
    with open(filename) as f:
        template = f.read()
    text = template.replace('{{data}}', data)
    with open('index.html','w') as f:
        f.write(text)

if __name__ == '__main__':
    main()

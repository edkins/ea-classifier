def main():
    with open('output.json') as f:
        data = f.read()
    with open('template.t') as f:
        template = f.read()
    text = template.replace('{{data}}', data)
    with open('index.html','w') as f:
        f.write(text)

if __name__ == '__main__':
    main()

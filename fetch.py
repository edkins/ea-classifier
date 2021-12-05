import base64
import json
import os
import os.path
import requests

def fetch(offset, limit, start_date, end_date):
    query = """
query fetch_forum_posts($terms:JSON) {
    posts(input: {
        terms: $terms
    }) {
        results {
            pageUrl
            title
            user {
                username
            }
            postedAt
            modifiedAt
            tags {
              name
            }
            htmlBody
        }
    }
}
"""
    response = requests.post('https://forum.effectivealtruism.org/graphql',
            json={
                'query': query,
                'variables': {
                    'terms': {
                        'limit':limit,
                        'offset':offset,
                        'after':start_date,
                        'before':end_date
                    }
                }})
    response.raise_for_status()
    obj = response.json()
    old = 0
    new = 0
    for post in obj['data']['posts']['results']:
        reformatted = json.dumps({
            'url': post['pageUrl'],
            'title': post['title'],
            'author': post['user']['username'],
            'datePosted': post['postedAt'],
            'dateModified': post['modifiedAt'],
            'tags': [t['name'] for t in post['tags']],
            'body': post['htmlBody']
        }, indent=4)
        filename = base64.urlsafe_b64encode(post['pageUrl'].encode('utf-8')).decode('utf-8')
        full_filename = f'data/{filename}.json'
        if os.path.exists(full_filename):
            old += 1
        else:
            new += 1
        with open(full_filename, 'w') as f:
            f.write(reformatted)
    return old, new

def main():
    os.makedirs('data', exist_ok=True)
    start_date = '2021-01-01'
    end_date = '2021-11-01'
    print(f'start_date = {start_date}, end_date = {end_date}')
    limit = 50
    offset = 0
    while True:
        old, new = fetch(offset=offset, limit=limit, start_date=start_date, end_date=end_date)
        print(f'offset = {offset}, limit = {limit}, old = {old}, new = {new}')
        if old > 0 or new == 0:
            break
        offset += limit

if __name__ == '__main__':
    main()

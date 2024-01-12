import requests
import sys
import json
from requests.auth import HTTPBasicAuth

def update_confluence(username, password, page_id, confluence_url, confluence_space, parent_page_id, content):
    url = f'{confluence_url}/{confluence_space}/rest/api/content/{page_id}'
    headers = {'Content-Type': 'application/json'}

    # Get the current content version
    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, password))
    response.raise_for_status()
    current_version = response.json()['version']['number']

    # Update the content
    payload = {
        'version': {'number': current_version + 1},
        'title': 'Updated Title',
        'type': 'page',
        'ancestors': [{'id': parent_page_id}],
        'body': {'storage': {'value': content, 'representation': 'storage'}}
    }

    response = requests.put(url, data=json.dumps(payload), headers=headers, auth=HTTPBasicAuth(username, password))
    response.raise_for_status()

if __name__ == '__main__':
    # Read inputs from command line arguments
    confluence_username = sys.argv[1]
    confluence_password = sys.argv[2]
    confluence_page_id = sys.argv[3]
    confluence_url = sys.argv[4]
    confluence_space = sys.argv[5]
    parent_page_id = sys.argv[6]
    release_tag = sys.argv[7]

    # Customize content based on your needs
    content = f'New release: {release_tag}'

    # Update Confluence on release
    update_confluence(confluence_username, confluence_password, confluence_page_id,
                       confluence_url, confluence_space, parent_page_id, content)

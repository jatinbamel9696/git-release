import requests
import argparse
import yaml

def load_config():
    with open("publisher/config/config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
    return config

def get_page_version(url, auth):
    response = requests.get(url, auth=auth)
    return response.json()["version"]["number"]

def update_confluence_page(login, password, page_id, release_info, confluence_url):
    confluence_url = f"{confluence_url}/content/{page_id}"
    auth = (login, password)

    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "version": {"number": get_page_version(confluence_url, auth)},
        "title": "Release Information",
        "type": "page",
        "body": {
            "storage": {"value": release_info, "representation": "storage"}
        },
    }

    response = requests.put(confluence_url, headers=headers, auth=auth, json=data)

    if response.status_code == 200:
        print("Confluence page updated successfully!")
    else:
        print(f"Failed to update Confluence page. Status code: {response.status_code}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Confluence page with release information.")
    parser.add_argument("--login", required=True, help="Confluence login")
    parser.add_argument("--password", required=True, help="Confluence password")
    parser.add_argument("--page-id", required=True, help="Confluence page ID to update")
    parser.add_argument("--release-info", required=True, help="Release information to update")

    args = parser.parse_args()

    config = load_config()
    update_confluence_page(args.login, args.password, args.page_id, args.release_info, config['confluence_url'])

import argparse
import logging
import requests
import yaml
from requests.auth import HTTPBasicAuth
from config.getconfig import getConfig

logging.basicConfig(level=logging.INFO)

def getConfig():
    with open("./publisher/config/config.yaml", "r") as yamlFileConfig:
        return yaml.safe_load(yamlFileConfig)

CONFIG = getConfig()

def searchPages(login, password, title):
    logging.info("Searching for pages with title: " + title)
    # Your search implementation here
    # Use the Confluence REST API to search for pages

def deletePages(pagesIDList, login, password):
    logging.info("Deleting pages: " + str(pagesIDList))
    # Your delete implementation here
    # Use the Confluence REST API to delete pages

def createPage(title, content, parentPageID, login, password):
    logging.info("Creating a new page: " + title)
    # Your create implementation here
    # Use the Confluence REST API to create a new page

def fetchGitHubReleaseNotes(token, owner, repo):
    headers = {'Authorization': f'token {token}'}
    response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/releases/latest', headers=headers)

    if response.status_code == 200:
        release_data = response.json()
        return release_data.get('body', '')
    else:
        logging.error(f"Failed to fetch GitHub release notes. Status code: {response.status_code}")
        return None

def publishGitHubReleaseToConfluence(login, password):
    github_token = CONFIG.get("GITHUB_TOKEN")
    github_owner = CONFIG.get("GITHUB_OWNER")
    github_repo = CONFIG.get("GITHUB_REPO")

    release_notes = fetchGitHubReleaseNotes(token=github_token, owner=github_owner, repo=github_repo)

    if release_notes is not None:
        search_result = searchPages(login=login, password=password, title=CONFIG["CONFLUENCE_PAGE_TITLE"])

        if search_result:
            deletePages(pagesIDList=search_result, login=login, password=password)

        createPage(title=CONFIG["CONFLUENCE_PAGE_TITLE"],
                   content=release_notes,
                   parentPageID=CONFIG["CONFLUENCE_PARENT_PAGE_ID"],
                   login=login,
                   password=password)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--login', help='Login with "" is mandatory', required=True)
    parser.add_argument('--password', help='Password with "" is mandatory', required=True)
    args = parser.parse_args()
    input_arguments = vars(args)

    publishGitHubReleaseToConfluence(login=input_arguments['login'],
                                     password=input_arguments['password'])
